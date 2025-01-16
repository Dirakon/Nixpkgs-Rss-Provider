#!/usr/bin/env bash

# ./cleanup.sh

STATE_PATH=$HOME/.local/state/nixpkgs-rss

# npx eoc init
npx eoc link
npx eoc dataize --alone app "$STATE_PATH"
