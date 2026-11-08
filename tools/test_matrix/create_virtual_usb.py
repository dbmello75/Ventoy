#!/usr/bin/env python3
"""Build a virtual USB from a compiled Ventoy Linux release, without raw disks."""
from contextlib import contextmanager
import hashlib
import lzma
import os
from pathlib import Path
import shutil
import stat
import struct
import subprocess
import tarfile
import tempfile

WORKSPACE = Path(os.environ.get("VTOY_WORKSPACE", Path(__file__).resolve().parents[2]))
SECTOR_SIZE = 512
PART1_START = 2048
PART2_SIZE = 65536


@contextmanager
def compiled_release():
    configured = os.environ.get("VTOY_PACKAGE_DIR")
    if configured:
        yield Path(configured)
        return
    packages = sorted([*(WORKSPACE / "INSTALL").glob("ventoy-*linux.tar.gz"), *(WORKSPACE / "release_artifacts").glob("ventoy-*linux.tar.gz")], key=lambda p: p.stat().st_mtime)
    if not packages:
        raise FileNotFoundError("Build a Linux release first, or set VTOY_PACKAGE_DIR to its extracted directory.")
    with tempfile.TemporaryDirectory(prefix="ventoy-package-") as tmp:
        with tarfile.open(packages[-1]) as archive:
            archive.extractall(tmp, filter="data")
        candidates = list(Path(tmp).glob("*/boot/boot.img"))
        if len(candidates) != 1:
            raise ValueError("The release archive must contain one boot/boot.img.")
        yield candidates[0].parents[1]


def create_image(release, output, data_size_mb=476, iso_paths=()):
    release, output = Path(release), Path(output)
    if data_size_mb < 16:
        raise ValueError("The data partition must be at least 16 MiB.")
    if output.is_symlink() or (output.exists() and not stat.S_ISREG(output.stat().st_mode)):
        raise ValueError("Output must be a regular image file.")
    boot = (release / "boot/boot.img").read_bytes()
    core = lzma.decompress((release / "boot/core.img.xz").read_bytes())
    efi = lzma.decompress((release / "ventoy/ventoy.disk.img.xz").read_bytes())
    if len(boot) < 446 or not core or len(core) > (PART1_START - 1) * SECTOR_SIZE:
        raise ValueError("Invalid Ventoy boot payload dimensions.")
    if len(efi) != PART2_SIZE * SECTOR_SIZE:
        raise ValueError("VTOYEFI must be exactly 32 MiB.")
    for tool in ("mkfs.ntfs", *( ["ntfscp"] if iso_paths else [] )):
        if not shutil.which(tool):
            raise FileNotFoundError(f"Required tool: {tool}")
    part1_size = data_size_mb * 2048
    part2_start = PART1_START + part1_size
    if part2_start + PART2_SIZE > 0xffffffff:
        raise ValueError("Virtual USB exceeds the MBR sector limit.")
    with tempfile.TemporaryDirectory(prefix="ventoy-partition-") as tmp:
        partition = Path(tmp) / "data.img"
        with partition.open("wb") as target:
            target.truncate(part1_size * SECTOR_SIZE)
        subprocess.run(["mkfs.ntfs", "-F", "-f", "-L", "Ventoy", "-H", "255", "-S", "63", "-p", str(PART1_START), str(partition)], check=True)
        for iso in sorted(map(Path, iso_paths)):
            subprocess.run(["ntfscp", str(partition), str(iso), "/" + iso.name], check=True)
        mbr = bytearray(512)
        mbr[:446] = boot[:446]
        mbr[384:400] = hashlib.sha256(boot + core).digest()[:16]
        struct.pack_into("<I", mbr, 440, 0x56544f59)
        for index, active, kind, start, length in [(0, 0x80, 0x07, PART1_START, part1_size), (1, 0, 0xef, part2_start, PART2_SIZE)]:
            struct.pack_into("<B3sB3sII", mbr, 446 + 16 * index, active, b"\xfe\xff\xff", kind, b"\xfe\xff\xff", start, length)
        mbr[510:512] = b"\x55\xaa"
        # Write a temporary regular file and replace the result only after success.
        with tempfile.NamedTemporaryFile(prefix=".ventoy-usb-", dir=output.parent, delete=False) as disk:
            scratch = Path(disk.name)
            try:
                disk.truncate((part2_start + PART2_SIZE) * SECTOR_SIZE)
                disk.write(mbr)
                disk.seek(SECTOR_SIZE)
                disk.write(core)
                disk.seek(PART1_START * SECTOR_SIZE)
                with partition.open("rb") as source:
                    shutil.copyfileobj(source, disk)
                disk.seek(part2_start * SECTOR_SIZE)
                disk.write(efi)
                disk.flush()
                os.replace(scratch, output)
            finally:
                scratch.unlink(missing_ok=True)
    print(f"Created virtual USB image: {output}")


def main():
    with compiled_release() as release:
        create_image(release, WORKSPACE / "ventoy_usb.img")


if __name__ == "__main__":
    main()
