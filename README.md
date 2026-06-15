# pit-alert
Scheduled News Alert System for Trading Pause Management.

# About

PIT ALERT is a Windows desktop application designed to help traders avoid entering or holding trades immediately before relevant economic news events.

The application reads the daily economic calendar, displays relevant events, and triggers a visual pop-up alert with a countdown before each configured event.

## Purpose

Many intraday traders avoid opening new positions minutes before high-impact economic news because price action can become unstable, volatile, or illiquid.

PIT ALERT acts as a behavioral safeguard: it creates a clear interruption before scheduled news events so the trader can pause, reassess, or avoid entering a trade during risky minutes.

## Current MVP Features

* Windows desktop application
* Economic calendar loaded from ForexFactory
* Local cache to reduce repeated web requests
* Daily events table
* Filters by currency/market
* Filters by impact level
* Configurable alert lead time
* Alert pop-up with countdown
* Countdown format: `mm:ss.mmm`
* One-shot alert sound
* Auto-close when countdown reaches zero
* Manual close button
* Draggable alert pop-up
* Alert ON/OFF control
* Visual configuration window
* Debug mode for internal testing

## Data Source

PIT ALERT currently uses ForexFactory as its only economic calendar source.

The app loads the weekly calendar, filters the events for the current local day, and displays the events matching the configured currencies and impact levels.

## Important Disclaimer

PIT ALERT does not provide trading advice, trade signals, investment recommendations, or market predictions.

The app only displays scheduled economic events and alerts the user before those events. Trading decisions remain the sole responsibility of the user.

## How to Run the Portable Version

If you received the portable version:

1. Extract the full `PIT_ALERT` folder.
2. Do not move only the `.exe` file.
3. Open:

```text
PIT_ALERT.exe
```

The full folder must remain together because the app depends on internal files, configuration, assets, and runtime libraries.

## Main Controls

### Alertas ON / OFF

Controls whether pop-up alerts are active.

* `Alertas ON`: the app will show pop-up alerts before future events.
* `Alertas OFF`: the app will keep showing the calendar but will not trigger pop-ups.

### Actualizar calendario

Reloads the economic calendar using the safe loading logic.

If a valid cache exists for the current day, the app uses the cache. If not, it attempts to retrieve the calendar from ForexFactory.

### Configuración

Opens the settings window.

From there, the user can configure:

* Time zone
* Alert minutes before the event
* Sound enabled/disabled
* Currencies
* Impact levels

## Default Configuration

The default configuration is stored in:

```text
config/settings.json
```

Example:

```json
{
  "timezone": "America/Mexico_City",
  "active_start": "07:00",
  "active_end": "13:00",
  "alert_minutes_before": 3,
  "currencies": ["USD", "CNY", "GBP", "JPY", "CAD", "EUR", "ALL"],
  "impacts": ["High", "Medium"],
  "sound_enabled": true,
  "auto_close_at_zero": true,
  "popup_width": 520,
  "popup_height": 300,
  "debug_mode": false
}
```

## Supported Currencies / Markets

Current configurable options:

* `ALL`
* `USD`
* `EUR`
* `CAD`
* `CNY`
* `GBP`
* `JPY`
* `AUD`
* `CHF`

`ALL` is used for events that affect all markets.

## Supported Impact Levels

Current configurable options:

* `High`
* `Medium`
* `Low`
* `Holiday`

Default:

```text
High, Medium
```

## Debug Mode

Debug mode enables internal testing buttons:

* `Probar popup 3 min`
* `Probar popup 10 seg`

To activate debug mode, edit:

```json
"debug_mode": true
```

To return to production mode:

```json
"debug_mode": false
```

Debug mode should remain disabled for normal user testing.

## Local Cache

PIT ALERT uses a local cache to avoid repeatedly requesting the calendar from ForexFactory.

Cache folder:

```text
data/cache/
```

This reduces the risk of receiving temporary web errors such as:

```text
429 Too Many Requests
```

If ForexFactory does not respond but a valid cache exists, the app may continue using cached data.

## Troubleshooting

### The table is empty

Possible causes:

1. No events match the selected currencies.
2. No events match the selected impact levels.
3. The local cache is outdated.
4. ForexFactory did not return new data.

Recommended steps:

1. Open `Configuración`.
2. Add more currencies.
3. Add `Low` impact temporarily.
4. Click `Actualizar calendario`.
5. Restart the app.

### The alert sound does not play

Check that the sound file exists:

```text
assets/pit_stop.wav
```

Also verify that sound is enabled in settings:

```json
"sound_enabled": true
```

### The app does not open

Make sure you are running the full portable folder, not only the `.exe`.

Do not separate:

```text
PIT_ALERT.exe
_internal/
assets/
config/
data/
```

depending on the generated build structure.

### Windows shows a security warning

This can happen because the app is not digitally signed yet.

For an internal MVP or pilot test, this is expected. For broader distribution, code signing should be considered.

## Development Setup

Recommended Python version:

```text
Python 3.11.x
```

Create virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the app:

```powershell
python app.py
```

## Build Portable EXE

Install dependencies:

```powershell
pip install -r requirements.txt
```

Clean previous builds:

```powershell
Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
Remove-Item -Force PIT_ALERT.spec -ErrorAction SilentlyContinue
```

Build with PyInstaller:

```powershell
pyinstaller `
  --name PIT_ALERT `
  --onedir `
  --windowed `
  --collect-all PySide6 `
  --add-data "assets;assets" `
  --add-data "config;config" `
  --add-data "data;data" `
  app.py
```

The portable build will be created in:

```text
dist/PIT_ALERT/
```

To distribute the app, compress and share the full folder:

```text
dist/PIT_ALERT/
```

Do not share only the `.exe`.

## Project Structure

```text
pit-alert/
├── app.py
├── requirements.txt
├── assets/
│   ├── gold-coin-sound.mp3
│   └── pit_stop.wav
├── config/
│   └── settings.json
├── core/
│   ├── event_model.py
│   └── settings.py
├── data/
│   └── cache/
├── sources/
│   └── forexfactory.py
└── ui/
    ├── alert_popup.py
    ├── main_window.py
    └── settings_window.py
```

## Current Limitations

* ForexFactory is the only data source.
* No automatic background startup with Windows yet.
* No system tray integration yet.
* No installer yet.
* No digital signature yet.
* No automatic update mechanism yet.
* No centralized logging or telemetry.
* No multi-user cloud configuration.

## Suggested Roadmap

### Version 0.2

* System tray mode
* Minimize to tray
* Right-click menu:

  * Open PIT ALERT
  * Alertas ON/OFF
  * Exit
* App icon
* Window icon
* Cleaner production UI

### Version 0.3

* Windows startup option
* Installer
* Better logging
* Export logs for troubleshooting
* More robust cache management

### Version 0.4

* Additional data source fallback
* Event search
* User-defined watchlists
* Market-specific presets

## Version

Current version:

```text
0.1.0 MVP
```

## License / Internal Use

This MVP is intended for internal testing and user feedback.

Before broader distribution, review licensing, data-source usage terms, code signing, and operational risk controls.
