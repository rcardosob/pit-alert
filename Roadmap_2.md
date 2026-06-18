# PIT ALERT — Professionalization Roadmap

## Product Vision

PIT ALERT will evolve from a portable MVP into a professional Windows desktop utility for traders.

The target behavior is similar to antivirus, VPN, or cloud-sync applications: the program should install cleanly, start automatically with Windows, run in the background, remain accessible from the system tray, and alert the trader before scheduled economic news events.

---

## Approved Product Decisions

### Installer

Approved installer technology:

```text
Inno Setup
```

The user should be able to download a setup file from GitHub Releases, double-click it, and install PIT ALERT without manually managing folders.

Expected installer artifact:

```text
PIT_ALERT_Setup_<version>.exe
```

---

### Installation Directory

Approved installation target:

```text
C:\Program Files\PIT ALERT\
```

This is the professional installation path for the application binaries.

Note: this installation mode may require administrator permissions.

---

### User Data Directories

The installed program should not store user configuration, cache, or logs inside `Program Files`.

Target structure:

```text
Program files:
C:\Program Files\PIT ALERT\

User configuration:
C:\Users\<usuario>\AppData\Roaming\PIT ALERT\settings.json

Cache:
C:\Users\<usuario>\AppData\Local\PIT ALERT\cache\

Logs:
C:\Users\<usuario>\AppData\Local\PIT ALERT\logs\
```

---

### Startup Behavior

Approved startup behavior:

```text
1. PIT ALERT starts automatically when Windows starts.
2. Alerts are ON by default on every Windows startup.
3. If the trader wants no alerts, they must manually disable alerts for that session.
```

Approved model:

```text
Modelo A — Seguridad operativa
```

Meaning:

```text
Every new Windows session starts with Alertas ON.
```

---

### System Tray Behavior

PIT ALERT should run as a resident app in the Windows system tray, next to the clock.

Approved tray menu:

```text
PIT ALERT
────────────────
Abrir PIT ALERT
Alertas ON
Alertas OFF
Actualizar calendario
────────────────
Salir
```

Not approved:

```text
Multiple tray icon color variants
```

The first professional version should use one tray icon only.

---

### Window Behavior

Approved behavior:

```text
1. The app can run even when the main window is hidden.
2. Closing the window does not terminate the app.
3. Closing the window hides/minimizes PIT ALERT to the system tray.
4. The app only closes completely when the user selects "Salir" from the tray menu.
```

---

### Single Instance

Approved.

PIT ALERT should prevent multiple instances.

Expected behavior:

```text
If PIT ALERT is already running and the user opens it again,
the existing window should be brought to the front instead of launching a second instance.
```

---

### Health Status

Approved.

The app should show a clear operational status, such as:

```text
Calendario actualizado: 07:02
Eventos pendientes: 5
Alertas: ON
Fuente: Web / Cache
```

---

### Logs

Approved.

The app should include basic logs to support troubleshooting.

Logs should capture:

```text
- App startup
- Startup mode: manual or Windows startup
- Initial alert status
- Calendar source: web or cache
- Number of events loaded
- Number of alerts scheduled
- Alert ON/OFF changes
- Popups shown
- Connection errors
- Sound errors
- App exit
```

---

### Temporary Silence Mode

Approved for a future version.

Potential future options:

```text
Silenciar 30 min
Silenciar 1 hora
Silenciar hasta mañana
```

This should not be included in the first system tray implementation.

---

### Test Alert Button

Not approved.

The current roadmap should not include a visible test alert option.

---

### Retry Strategy

Approved.

If the calendar source fails:

```text
1. Use local cache if available.
2. Avoid repeated aggressive web requests.
3. Show status: "Usando cache" or equivalent.
4. Retry later using controlled logic.
5. Log the failure.
```

---

### Digital Signature

Required later.

This will be addressed when the product reaches a more serious distribution stage.

Goal:

```text
Reduce Windows security warnings and increase trust during installation.
```

---

### GitHub Releases

Approved.

The distribution flow should be:

```text
1. Build application
2. Create installer
3. Upload installer to GitHub Releases
4. User downloads setup file
5. User installs PIT ALERT
6. PIT ALERT starts automatically with Windows
```

---

# Version Roadmap

## Version 0.2 — Resident App / System Tray

### Objective

Convert PIT ALERT from a normal desktop window into a resident background utility.

### Scope

```text
- Add system tray icon
- Add approved tray menu
- Open PIT ALERT from tray
- Turn Alertas ON from tray
- Turn Alertas OFF from tray
- Update calendar from tray
- Exit app from tray
- Closing the main window hides it instead of killing the app
- "Salir" from tray is the real shutdown path
- Alerts start ON by default
```

### Approved Tray Menu

```text
PIT ALERT
────────────────
Abrir PIT ALERT
Alertas ON
Alertas OFF
Actualizar calendario
────────────────
Salir
```

### Likely Files Affected

```text
app.py
ui/main_window.py
core/settings.py
```

Possible new file:

```text
ui/tray_controller.py
```

### Acceptance Criteria

```text
- App opens normally in development mode
- Tray icon appears next to Windows clock
- Tray menu works
- "Abrir PIT ALERT" shows the main window
- "Alertas ON" activates alerts
- "Alertas OFF" disables alerts
- "Actualizar calendario" reloads calendar
- Clicking X hides the window but app keeps running
- "Salir" closes the app completely
```

---

## Version 0.3 — Single Instance + Startup Behavior

### Objective

Prevent duplicate alert scheduling and prepare the app for automatic startup.

### Scope

```text
- Prevent multiple PIT ALERT instances
- If app is already running, opening it again brings existing window to front
- Ensure alerts start ON by default at every session start
- Prepare startup mode logic for installer integration
```

### Acceptance Criteria

```text
- Opening PIT ALERT twice does not create duplicate app processes
- Duplicate alerts are not scheduled
- Existing window is shown when user tries to open app again
- App starts with Alertas ON by default
```

---

## Version 0.4 — Logs and Health Status

### Objective

Make PIT ALERT operationally diagnosable.

### Scope

```text
- Add local log file
- Add health status to UI
- Log app startup
- Log calendar load
- Log source: web/cache
- Log alert scheduling
- Log popups shown
- Log alert ON/OFF changes
- Log connection failures
- Log sound failures
```

### Target Log Directory

```text
C:\Users\<usuario>\AppData\Local\PIT ALERT\logs\
```

### Target Health Status

```text
Calendario actualizado: HH:MM
Eventos pendientes: N
Alertas: ON/OFF
Fuente: Web/Cache
```

### Acceptance Criteria

```text
- Log file is created automatically
- Logs are readable as plain text
- Calendar updates are logged
- Alert state changes are logged
- Popup events are logged
- UI displays useful operational status
```

---

## Version 0.5 — Professional User Data Directories

### Objective

Separate application binaries from user-specific data.

### Scope

Move runtime data from the project/install folder into Windows user directories.

### Target Structure

```text
Program files:
C:\Program Files\PIT ALERT\

Configuration:
C:\Users\<usuario>\AppData\Roaming\PIT ALERT\settings.json

Cache:
C:\Users\<usuario>\AppData\Local\PIT ALERT\cache\

Logs:
C:\Users\<usuario>\AppData\Local\PIT ALERT\logs\
```

### Acceptance Criteria

```text
- App reads settings from AppData Roaming
- App writes cache to AppData Local
- App writes logs to AppData Local
- Program Files remains read-only for runtime data
- Existing settings can be migrated or recreated safely
```

---

## Version 0.6 — Inno Setup Installer

### Objective

Create a real Windows installer with uninstaller.

### Scope

```text
- Build PyInstaller output
- Create Inno Setup script
- Install to C:\Program Files\PIT ALERT\
- Create Start Menu shortcut
- Optional desktop shortcut
- Register uninstaller
- Register startup with Windows
- Use pit_alert.ico as installer/app icon
```

### Installer Output

```text
PIT_ALERT_Setup_0.6.0.exe
```

### Startup Registration

The installer should register PIT ALERT to start automatically when the user logs into Windows.

Likely registry target:

```text
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
```

### Acceptance Criteria

```text
- User can install PIT ALERT with double click
- App is installed in Program Files
- Start Menu shortcut exists
- Uninstaller exists
- PIT ALERT starts automatically after Windows login
- PIT ALERT starts with Alertas ON
- App appears in system tray
```

---

## Version 0.7 — GitHub Releases Distribution

### Objective

Distribute PIT ALERT professionally through GitHub Releases.

### Scope

```text
- Create release tag
- Attach installer .exe
- Include release notes
- Include version number
- Include installation instructions
- Include known limitations
```

### Release Artifact

```text
PIT_ALERT_Setup_0.7.0.exe
```

### Acceptance Criteria

```text
- GitHub Release contains installer
- User can download installer directly
- Installation flow works from downloaded file
- Release notes document changes clearly
```

---

## Version 0.8 — Temporary Silence and Retry Improvements

### Objective

Improve trader control and calendar reliability.

### Scope

```text
- Add temporary silence mode
- Add controlled retry logic
- Improve cache fallback messaging
- Avoid aggressive repeated requests
```

### Future Silence Options

```text
Silenciar 30 min
Silenciar 1 hora
Silenciar hasta mañana
```

### Acceptance Criteria

```text
- Trader can silence alerts temporarily
- Alerts resume automatically after silence window
- Calendar failures use cache when possible
- Status clearly explains whether data comes from web or cache
- Failures are logged
```

---

## Version 0.9 — Digital Signature and Distribution Trust

### Objective

Reduce Windows trust warnings and prepare for broader external distribution.

### Scope

```text
- Obtain code signing certificate
- Sign executable
- Sign installer
- Validate Windows SmartScreen behavior
- Document publisher identity
```

### Acceptance Criteria

```text
- Installer is digitally signed
- Executable is digitally signed
- Windows shows verified publisher when possible
- Distribution friction is reduced
```

---

## Version 1.0 — Stable Professional Release

### Objective

Deliver a stable, professional, user-installable PIT ALERT release.

### Expected Capabilities

```text
- Installer
- Uninstaller
- Program Files installation
- System tray operation
- Automatic Windows startup
- Alerts ON by default
- Single instance
- User settings in AppData
- Cache in AppData
- Logs in AppData
- Health status
- GitHub Releases distribution
- Signed installer/executable if available
```

---

# Implementation Order

Recommended implementation sequence:

```text
1. System tray minimum
2. Close-to-tray behavior
3. Real exit from tray
4. Alertas ON by default
5. Single instance
6. Logs
7. Health status
8. AppData directory migration
9. Rebuild PyInstaller
10. Inno Setup installer
11. Windows auto-start registration
12. GitHub Release
13. Temporary silence
14. Retry improvements
15. Digital signature
```

---

# Immediate Next Step

Start with:

```text
Version 0.2 — Resident App / System Tray
```

First technical milestone:

```text
Add QSystemTrayIcon with the approved menu and make "Cerrar ventana" hide PIT ALERT instead of closing it.
```

Approved tray menu:

```text
PIT ALERT
────────────────
Abrir PIT ALERT
Alertas ON
Alertas OFF
Actualizar calendario
────────────────
Salir
```
