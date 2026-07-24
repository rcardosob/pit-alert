# Changelog

## 0.2.1 - 2026-07-24

- Replaced application icon with new transparent icon (`pit_alert2.ico`).
- Added System Tray support (minimizes to notification area on window close).
- Added tray context menu with 'Open', 'Alerts ON/OFF' toggle, and 'Exit' options.
- Added dynamic tray tooltip showing the next upcoming economic event and countdown.
- Added 'Start Minimized' option in the Settings window.
- Cleaned up main UI layout by removing redundant status text label.

## 0.2.0 - 2026-07-10

- Added a Windows installer built with Inno Setup.
- Added installation in Program Files, Start Menu access, optional Desktop shortcut, and uninstaller.
- Moved per-user settings and calendar cache to `%LOCALAPPDATA%\PIT ALERT`.
- Preserved the existing calendar, alert, sound, and configuration behavior.
- Replaced the Apache 2.0 license with the PIT ALERT Community License 1.0.
