# Plan de Implementación: System Tray Icon (Pit-Alert)

## Objetivo
Configurar la aplicación PySide6 para que no se cierre completamente al presionar la "X", sino que se minimice al área de notificaciones de Windows (System Tray) y continúe monitoreando eventos en segundo plano.

---

## Modificaciones Técnicas Clave

1. **Persistencia de la Aplicación:**
   Configurar `app.setQuitOnLastWindowClosed(False)` para evitar que Qt termine el proceso cuando la ventana principal se oculta.

2. **Interceptación de Cierre (`closeEvent`):**
   Sobrescribir el evento `closeEvent` en `QMainWindow` ejecutando `event.ignore()` y `self.hide()`.

3. **Interacción con el Usuario (Estándar Windows):**
   * **Clic Izquierdo / Doble Clic:** Muestra / Oculta la ventana principal (`showNormal()` / `hide()`).
   * **Clic Derecho:** Abre el menú contextual (`QMenu`) con las opciones de control rápido.

---

## Código de Referencia (PySide6)

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction

class PitAlertWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pit-Alert")
        self.resize(400, 300)

        # 1. Configurar el ícono del System Tray
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("ruta_a_tu_icono.ico"))  # Requerido para visibilidad
        self.tray_icon.setToolTip("Pit-Alert: Monitoreo Activo")

        # 2. Crear el menú contextual (Clic Derecho)
        self.tray_menu = QMenu()
        
        # Opciones del menú
        self.action_abrir = QAction("Abrir Pit-Alert", self)
        self.action_abrir.triggered.connect(self.showNormal)
        
        self.action_alertas = QAction("Alertas ON/OFF", self)
        self.action_alertas.setCheckable(True)
        self.action_alertas.setChecked(True)
        self.action_alertas.toggled.connect(self.toggle_alertas)
        
        self.action_cerrar = QAction("Cerrar definitivamente", self)
        self.action_cerrar.triggered.connect(QApplication.instance().quit)
        
        # Ensamblar menú
        self.tray_menu.addAction(self.action_abrir)
        self.tray_menu.addAction(self.action_alertas)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.action_cerrar)
        
        # Asignar menú contextual al ícono
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        # 3. Capturar Clic Izquierdo (Abrir/Ocultar ventana)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def closeEvent(self, event):
        """Intercepta el botón de cerrar (X) para ocultar la ventana."""
        event.ignore()
        self.hide()

    def on_tray_icon_activated(self, reason):
        """Maneja el clic izquierdo sobre el ícono de la barra de tareas."""
        if reason == QSystemTrayIcon.Trigger:
            if self.isHidden():
                self.showNormal()
                self.activateWindow()
            else:
                self.hide()

    def toggle_alertas(self, estado):
        """Lógica para pausar/reanudar el motor de alertas."""
        if estado:
            print("[Info] Alertas reanudadas.")
        else:
            print("[Info] Alertas pausadas.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Previene el cierre del proceso al ocultar la última ventana
    app.setQuitOnLastWindowClosed(False)
    
    window = PitAlertWindow()
    window.show()
    
    sys.exit(app.exec())
    