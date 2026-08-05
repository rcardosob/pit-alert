from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtNetwork import QLocalServer, QLocalSocket
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

    socket_name = "pit_alert_single_instance_key"

    # Intentar conectar con una instancia que ya esté corriendo
    socket = QLocalSocket()
    socket.connectToServer(socket_name)
    if socket.waitForConnected(500):
        # Ya está corriendo. Mandar comando para mostrar ventana y salir.
        socket.write(b"show")
        socket.waitForBytesWritten(1000)
        socket.disconnectFromServer()
        return 0

    # Si no hay otra instancia, levantar el servidor local
    server = QLocalServer()
    server.removeServer(socket_name)  # Limpiar en caso de un crash previo
    if not server.listen(socket_name):
        pass

    app.setQuitOnLastWindowClosed(False)

    icon_path = resource_path("assets/icons/pit_alert2.ico")
    app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow(icon_path=icon_path)
    window.setWindowIcon(QIcon(str(icon_path)))

    # Callback para manejar conexiones de nuevas instancias que intenten abrirse
    def handle_new_connection():
        client_socket = server.nextPendingConnection()
        if client_socket:
            if client_socket.waitForReadyRead(500):
                msg = client_socket.readAll().data().decode("utf-8")
                if msg == "show":
                    window.restore_from_tray()
            client_socket.disconnectFromServer()
            client_socket.deleteLater()

    server.newConnection.connect(handle_new_connection)

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

    # Guardar referencia del servidor para que no lo limpie el recolector de basura
    app.server = server

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())