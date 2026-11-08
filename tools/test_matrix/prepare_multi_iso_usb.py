#!/usr/bin/env python3
"""Prepare a virtual USB with test ISOs using actual release boot payloads."""
import os
from pathlib import Path
from create_virtual_usb import WORKSPACE, compiled_release, create_image


def main():
    iso_dir = Path(os.environ.get("VTOY_ISO_DIR", "/tmp/iso_test_set"))
    images = sorted(iso_dir.glob("*.iso"))
    if not images:
        raise FileNotFoundError(f"No test ISOs in {iso_dir}.")
    required_mb = (sum(p.stat().st_size for p in images) + (1 << 20) - 1) // (1 << 20)
    data_size_mb = max(1024, required_mb + max(512, required_mb // 10))
    with compiled_release() as release:
        create_image(release, WORKSPACE / "ventoy_usb.img", data_size_mb, images)


if __name__ == "__main__":
    main()
