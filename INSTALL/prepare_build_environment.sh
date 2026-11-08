#!/bin/sh
set -eu
ventoy_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
command -v docker >/dev/null 2>&1 || { echo "Install Docker before preparing the build environment." >&2; exit 1; }
exec docker build -t ventoy-repro -f "$ventoy_root/Dockerfile.reproducible" "$ventoy_root"
