#!/usr/bin/env python3
"""Non-destructive checks for the community PR integration."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def run(*args, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, **kwargs)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def main():
    locales = [ROOT / "LANGUAGES/languages.json", *sorted((ROOT / "INSTALL/grub/menu").glob("*.json"))]
    for path in locales:
        json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)
    languages = json.loads(locales[0].read_text())
    names = [item["name"] for item in languages]
    assert len(names) == len(set(names)), "Duplicate locale names"
    assert names == sorted(names, key=str.lower), "Locale order"
    english = json.loads((ROOT / "INSTALL/grub/menu/en_US.json").read_text())
    for path in locales[1:]:
        assert english.keys() <= json.loads(path.read_text()).keys(), f"Missing keys: {path}"
    for path in ROOT.rglob("*.udisks.inc"):
        assert path.with_name(path.name.removesuffix(".udisks.inc")).is_file()
    run("node", "--check", "LinuxGUI/WebUI/static/js/vtoy.js")
    with tempfile.TemporaryDirectory(prefix="ventoy-check-") as tmp:
        exe = str(Path(tmp) / "json_escape_test")
        flags = ["-fsanitize=address,undefined", "-fno-omit-frame-pointer"] if os.environ.get("VTOY_SANITIZE") == "1" else []
        run("gcc", "-std=gnu99", "-O1", "-g", "-ffunction-sections", "-fdata-sections", *flags,
            "-IPlugson/src/Core", "Plugson/src/Core/ventoy_json.c", "tests/integration/json_escape_test.c",
            "-Wl,--gc-sections", "-o", exe)
        output = run(exe, capture_output=True).stdout.decode("utf-8")
        rows = output.splitlines()
        for row in rows:
            assert row.endswith(",")
            json.loads(row[:-1])
        assert len(rows) > 2000
        locale_exe = str(Path(tmp) / "locale_list_test")
        run("gcc", "-std=gnu99", "-O1", "-g", *flags, "-IPlugson/src/Web",
            "tests/integration/locale_list_test.c", "-o", locale_exe)
        run(locale_exe)
        empty_workspace = Path(tmp) / "no-release"
        empty_workspace.mkdir()
        env = dict(os.environ, VTOY_WORKSPACE=str(empty_workspace))
        env.pop("VTOY_PACKAGE_DIR", None)
        missing_release = subprocess.run(
            ["python3", str(ROOT / "tools/test_matrix/create_virtual_usb.py")],
            env=env, capture_output=True)
        assert missing_release.returncode != 0
        assert not (empty_workspace / "ventoy_usb.img").exists()
    print(f"PASS: {len(locales)} JSON files, {len(languages)} locales, JS syntax, optional backend layout, {len(rows)} JSON buffer cases")


if __name__ == "__main__":
    main()
