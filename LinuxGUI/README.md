# Linux GUI

The build scripts select the native GTK, Qt or WebUI backend.

## Optional UDisks2 / Flatpak backend

The native backend remains the default. The community UDisks2 port from upstream
PR #3319 is available with `make -C LinuxGUI gtk3` and requires the `udisks2` and
`gtk+-3.0` development packages plus pkg-config. It selects the alternative source
files with `VTOY_USE_UDISKS`. The Flatpak manifest is experimental.

This backend has not been validated against physical disks in this integration.
Test installation, update, unmounting and permissions with disposable virtual
disks before using it with data.
