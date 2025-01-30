## Information

RSS provider for [NixPkgs](https://github.com/NixOS/nixpkgs) used to monitor version changes of specific packages on specific NixPkgs branches.

## Requirements

All requirements are specified through nix, so you can use it to get all the requirements. `nix develop` or `direnv allow`.

Alternatively, you could manually install `npm`, `python3` (with `flask`) and `jdk` (note the specific versions used in `flake.nix` and `flake.lock` for better reproducability)

## Usage

Before first launch you obviously need to install npm dependencies:
```bash
npm i
```

Afterwards, use:
```bash
./src/orchestrator.py
```

If some sudden problems arise, you could also use cleanup helper script that removes all potentially broken cache:
```bash
./cleanup.sh
```

## License

This Project is licensed under the MIT License. Check license file for more info.
