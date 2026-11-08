#!/bin/bash
set -euo pipefail

ventoy_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
verify_workspace=$(mktemp -d "${TMPDIR:-/tmp}/ventoy-repro.XXXXXX")
trap 'rm -rf -- "$verify_workspace"' EXIT

artifacts=(
    INSTALL/ventoy/vtoyjump64.exe
    INSTALL/ventoy/vtoyjump32.exe
    INSTALL/EFI/BOOT/fbx64.efi
    INSTALL/ventoy/ventoy_x64.efi
    INSTALL/ventoy/vtoyutil_x64.efi
    IMG/ventoy.cpio
    Unix/ventoy_unix.cpio
)

for pass in a b; do
    build_dir="$verify_workspace/$pass"
    git clone --quiet --no-hardlinks "$ventoy_root" "$build_dir"
    # A checked-in binary cannot count as evidence of a successful rebuild.
    for artifact in "${artifacts[@]}"; do
        rm -f -- "$build_dir/$artifact"
    done
    (
        cd "$build_dir"
        umask 0022
        export SOURCE_DATE_EPOCH=1700000000 LC_ALL=C TZ=UTC
        bash build_reproducible.sh
    ) >"$verify_workspace/$pass.log" 2>&1 || {
        cat "$verify_workspace/$pass.log" >&2
        echo "Reproducibility pass $pass failed to build." >&2
        exit 1
    }
done

failed=0
for artifact in "${artifacts[@]}"; do
    if [ ! -s "$verify_workspace/a/$artifact" ] || [ ! -s "$verify_workspace/b/$artifact" ]; then
        echo "FAIL: missing or empty artifact: $artifact" >&2
        failed=1
    elif ! cmp -s "$verify_workspace/a/$artifact" "$verify_workspace/b/$artifact"; then
        echo "FAIL: different output: $artifact" >&2
        failed=1
    else
        echo "PASS: identical rebuilt artifact: $artifact"
    fi
done
exit "$failed"
