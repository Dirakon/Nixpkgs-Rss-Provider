#!/usr/bin/env python3

import subprocess
import re
import sys
import threading

LINE_COUNT_PATTERN = re.compile(r'^\(lines: (\d+)\)$')

def stderr_reader(proc):
    """Read stderr from the subprocess and write to script's stderr."""
    while True:
        line = proc.stderr.readline()
        if not line:
            break
        sys.stderr.write(line)
        sys.stderr.flush()

def parse_multiline(stream):
    """Parse multiline input with (lines: N) format from given stream."""
    size_defining_line = stream.readline().rstrip('\n')
    match = LINE_COUNT_PATTERN.match(size_defining_line)
    if not match:
        return None
    try:
        n = int(match.group(1))
    except ValueError:
        return None
    
    return [stream.readline().rstrip('\n') for _ in range(n)]

def write_multiline(stream, lines):
    """Write multiline output with (lines: N) format to given stream."""
    stream.write(f"(lines: {len(lines)})\n")
    for line in lines:
        stream.write(f"{line}\n")
    stream.flush()

def get_rss(proc, branch, program_name, version):
    while True:
        line = proc.stdout.readline()
        if not line:  # EOF
            break
        line = line.rstrip('\n')

        if line.startswith("Request: "):
            if line == "Request: program-name":
                proc.stdin.write(f"{program_name}\n")
                proc.stdin.flush()
            elif line == "Request: branch":
                proc.stdin.write(f"{branch}\n")
                proc.stdin.flush()
            elif line.startswith("Request: get-version|||"):
                proc.stdin.write(f"{version}\n")
                proc.stdin.flush()
            elif line.startswith("Request: write-file|||"):
                parts = line.split('|||')
                file_path = parts[1].strip()
                content = parse_multiline(proc.stdout)
                if content is not None:
                    try:
                        with open(file_path, 'w') as f:
                            f.write('\n'.join(content))
                        proc.stdin.write("OK\n")
                        proc.stdin.flush()
                    except IOError:
                        pass  # Handle file write error silently
            elif line.startswith("Request: read-file|||"):
                parts = line.split('|||')
                file_path = parts[1].strip()
                try:
                    with open(file_path, 'r') as f:
                        content = f.read().splitlines()
                except IOError:
                    content = []
                write_multiline(proc.stdin, content)
        elif line == "Log:":
            logs = parse_multiline(proc.stdout)
            if logs is not None:
                for log_line in logs:
                    print(f'-{log_line}')
        elif line == "Rss:":
            rss_lines = parse_multiline(proc.stdout)
            print("Final RSS is as follows:")
            if rss_lines is not None:
                for rss_line in rss_lines:
                    print(rss_line)
                return '\n'.join(rss_lines)
            return None

def main():
    # Start the subprocess
    proc = subprocess.Popen(
        ["./run.sh"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )

    # Start stderr reader thread
    stderr_thread = threading.Thread(target=stderr_reader, args=(proc,))
    stderr_thread.daemon = True
    stderr_thread.start()

    while True:
        program = input("program: ")
        branch = input("branch: ")
        current_version = input("current version: ")
        rss = get_rss(proc, branch, program, current_version)

    # Wait for the subprocess to terminate
    proc.wait()

if __name__ == "__main__":
    main()
