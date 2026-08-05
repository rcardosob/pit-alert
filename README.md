# PIT ALERT

> **Situational Awareness for Traders.**  
> *Sometimes the best trade is leaving the track.*

[![Version](https://img.shields.io/badge/version-v0.2.2-C9A227.svg?style=flat-square)](https://github.com/rcardosob/pit-alert/releases)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0078D4.svg?style=flat-square)](https://github.com/rcardosob/pit-alert/releases)
[![Category](https://img.shields.io/badge/category-Trading%20%2F%20Risk%20Safeguard-27272A.svg?style=flat-square)](#about)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)

[🌐 **Official Interactive Campaign & Web**](https://fin.mithril.mx/pit-alert/) | [📥 **Download Desktop App (v0.2.2)**](https://fin.mithril.mx/pit-alert/PIT_ALERT_Setup_0.2.2.exe)

---

## About

**PIT ALERT** is a specialized Windows desktop application designed to act as a behavioral safeguard for intraday traders during volatile economic news events.

In high-frequency and intraday trading, scheduled economic releases (such as **CPI, FOMC rate decisions, NFP, GDP, and inflation reports**) can generate sudden market instability, extreme spread widening, and severe slippage within milliseconds.

Traders heavily focused on price action, chart patterns, and trade execution can easily lose track of the economic calendar. **PIT ALERT monitors scheduled economic releases in the background and issues high-visibility visual & audible warnings before an event occurs**, allowing traders to pause execution, protect open positions, or step back before volatility arrives.

Conceptually, **PIT ALERT is the Pit Wall for traders**:
* **The Trader** is the driver watching the market.
* **PIT ALERT** watches the track and warns when external conditions are about to change.

---

## Core Product Positioning

PIT ALERT is **NOT** a trading indicator, signal generator, or advisory bot.

| 🟢 What PIT ALERT Does | 🔴 What PIT ALERT Refuses To Do |
| :--- | :--- |
| **Monitors** scheduled economic events in real time. | **No predictions** or directional bias. |
| **Warns** the trader before high-impact news releases. | **No BUY / SELL signals**. |
| **Issues** a prominent pop-up with precise `mm:ss` countdown. | **No trading advice** or execution recommendations. |
| **Protects attention**, letting traders focus purely on execution. | **Does NOT tell the trader what to do**. |

> *Entering the pits does not mean abandoning the race. It is a tactical decision.*

---

## Key Features

* **Desktop Native Interface:** Lightweight Windows desktop application built with Python & PySide6.
* **ForexFactory Calendar Source:** Real-time data sync for economic releases.
* **Smart Local Caching Layer:** Reduces unnecessary web requests and ensures offline availability of previously fetched daily calendars.
* **Custom Currency & Impact Filters:** Focus strictly on relevant markets (USD, EUR, GBP, JPY, CAD, etc.) and impact levels (**HIGH**, **MEDIUM**, **LOW**).
* **Countdown Alert Pop-up:** Frameless, stay-on-top alert window with active `mm:ss` event countdown.
* **Audible Warning:** One-shot tactical pit stop audio chime (`pit_stop.wav`) on alert activation.
* **Configurable Anticipation:** Define how many minutes prior to an event the warning triggers.
* **System Tray Minimization:** Runs silently in the background without cluttering workspace monitors.

---

## Visual Architecture

### Desktop Application
The desktop interface features a high-contrast dark theme designed to fit alongside professional trading platforms (MetaTrader, TradingView, NinjaTrader, Sierra Chart).

```
+-----------------------------------------------------------------------------------+
|  PIT ALERT — Economic News Alert System                                   [_][Square][X]  |
+-----------------------------------------------------------------------------------+
|  [ Alerts ON ]    [ Refresh Calendar ]    [ Settings ]                            |
+-----------------------------------------------------------------------------------+
|  Local Time  | Currency | Impact    | Event                        | Alert        |
+--------------+----------+-----------+------------------------------+--------------+
|  14:30       | USD      | HIGH      | Core CPI (MoM)               | IN 3 MIN     |
|  15:00       | USD      | HIGH      | Existing Home Sales          | Scheduled    |
|  16:30       | EUR      | MEDIUM    | ECB President Speaks         | Scheduled    |
+-----------------------------------------------------------------------------------+
```

---

## Installation Guide (Windows)

### Option 1: Installer (Recommended)
1. Download [PIT_ALERT_Setup_0.2.1.exe](https://fin.mithril.mx/pit-alert/PIT_ALERT_Setup_0.2.1.exe).
2. Run the installer and follow the prompt.
3. Launch **PIT ALERT** from your Start Menu or Desktop shortcut.

### Option 2: Portable Build
1. Download `PIT_ALERT_Portable_0.2.1.zip` from [Releases](https://github.com/rcardosob/pit-alert/releases).
2. Extract to any directory and execute `PIT_ALERT.exe`.

---

## Technical Stack & Architecture

* **Core Language:** Python 3.11+
* **GUI Engine:** PySide6 (Qt 6 for Python)
* **Calendar Data:** ForexFactory Calendar Source
* **Packaging:** PyInstaller & Inno Setup
* **Web Landing Page:** Vite, Vanilla JS, GSAP (ScrollTrigger), CSS3

### Project Structure

```
pit-alert/
├── app.py                      # Main entry point
├── core/                       # Core logic, settings, models & cache paths
│   ├── event_model.py
│   ├── settings.py
│   └── paths.py
├── sources/                    # Data sources (ForexFactory fetcher)
│   └── forexfactory.py
├── ui/                         # PySide6 Desktop GUI components
│   ├── main_window.py
│   ├── alert_popup.py
│   └── settings_window.py
├── docs/                       # Project documentation & design briefs
│   └── design/                 # Creative Brief, Proposal & Storyboard
├── landing/                    # Web Landing Page source code (Vite + GSAP)
└── installer/                  # Inno Setup build configurations
```

---

## Development Setup

To run PIT ALERT locally for development or customization:

```bash
# Clone the repository
git clone https://github.com/rcardosob/pit-alert.git
cd pit-alert

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run desktop application
python app.py
```

### Running the Web Landing Page

```bash
cd landing
npm install
npm run dev
```

---

## Disclaimer

**PIT ALERT** does not provide investment advice, trading signals, or market predictions. Economic calendar releases are provided for informational and situational awareness purposes only. Trading decisions remain the sole responsibility of the user.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

© 2026 **MITHRIL MOUNTAIN®** — All Rights Reserved.
