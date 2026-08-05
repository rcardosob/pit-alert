# Changelog

## 0.2.2 - 2026-08-05

- Added "Hora NY" column in the main economic calendar table to track New York trading time.
- Added post-event audio warning (`two_minutes__engine_fire_up_.wav`) playing exactly 3 minutes after each news event.
- Added automatic visual gray-out effect for past news events and their badges.
- Added native Windows startup auto-start registry integration, enabled by default with a setting to disable it.
- Added Single Instance execution guard using local socket to prevent running multiple app instances.

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
