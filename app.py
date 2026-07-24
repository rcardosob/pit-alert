from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QSystemTrayIcon

from ui.main_window import MainWindow


def resource_path(relative_path: str) -> Path:
    """
    Resolve paths correctly both in development mode and in PyInstaller builds.
    """
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base_path / relative_path


def main() -> int:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    icon_path = resource_path("assets/icons/pit_alert2.ico")
    app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow(icon_path=icon_path)
    window.setWindowIcon(QIcon(str(icon_path)))

    if window.settings.get("start_minimized", False):
        window.hide()
        if hasattr(window, "tray_icon") and window.tray_icon.supportsMessages():
            window.tray_icon.showMessage(
                "PIT ALERT",
                "Iniciado en segundo plano en el System Tray.",
                QSystemTrayIcon.MessageIcon.Information,
                3000,
            )
    else:
        window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())