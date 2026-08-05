import sys
from pathlib import Path
from datetime import datetime, timedelta
from functools import partial
from zoneinfo import ZoneInfo

from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QFont, QIcon, QAction, QColor
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QSystemTrayIcon,
    QMenu,
)

from core.event_model import EconomicEvent
from core.settings import load_settings
from sources.forexfactory import fetch_forexfactory_events, ForexFactoryError
from ui.alert_popup import AlertPopup
from ui.settings_window import SettingsWindow


class MainWindow(QMainWindow):
    def __init__(self, icon_path: Path | str | None = None) -> None:
        super().__init__()

        self.settings = load_settings()
        self.events: list[EconomicEvent] = []
        self.alerted_events: set[str] = set()
        self.active_popups: list[AlertPopup] = []
        self.alert_timers: dict[str, QTimer] = {}
        self.post_event_timers: dict[str, QTimer] = {}
        self.played_post_event_sounds: set[str] = set()
        self.active_sound_effects: list[QSoundEffect] = []

        self.alerts_enabled = True
        self.is_closing = False
        self.has_shown_tray_message = False
        self.last_calendar_status = "Calendario no cargado."

        self.setWindowTitle("PIT ALERT")
        self.resize(980, 620)

        self._build_ui()
        self._apply_styles()
        self._update_alerts_button_style()
        self._setup_tray_icon(icon_path)

        self.tooltip_timer = QTimer(self)
        self.tooltip_timer.timeout.connect(self._update_tray_tooltip)
        self.tooltip_timer.start(60000)

        # Sincronizar registro de Windows al iniciar
        from core.settings import update_windows_autostart
        update_windows_autostart(self.settings.get("disable_autostart", False))

        self.load_forexfactory_calendar(force_refresh=False)

    def _build_ui(self) -> None:
        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(22, 22, 22, 22)
        root.setSpacing(18)

        header = QLabel("PIT ALERT")
        header.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        subtitle = QLabel("Economic news alert system for traders")
        subtitle.setFont(QFont("Arial", 11))

        button_row = QHBoxLayout()

        self.alerts_toggle_button = QPushButton("Alertas ON")
        self.alerts_toggle_button.clicked.connect(self.toggle_alerts)

        self.refresh_button = QPushButton("Actualizar calendario")
        self.refresh_button.clicked.connect(self.refresh_calendar)

        self.settings_button = QPushButton("Configuración")
        self.settings_button.clicked.connect(self.open_settings)

        button_row.addWidget(self.alerts_toggle_button)
        button_row.addWidget(self.refresh_button)
        button_row.addWidget(self.settings_button)

        if self.settings.get("debug_mode", False):
            self.test_popup_button = QPushButton("Probar popup 3 min")
            self.test_popup_button.clicked.connect(self.show_test_popup)

            self.fast_popup_button = QPushButton("Probar popup 10 seg")
            self.fast_popup_button.clicked.connect(self.show_fast_popup)

            self.test_audio2_button = QPushButton("Probar Audio 2")
            self.test_audio2_button.clicked.connect(self.play_test_audio2)

            button_row.addWidget(self.test_popup_button)
            button_row.addWidget(self.fast_popup_button)
            button_row.addWidget(self.test_audio2_button)

        button_row.addStretch(1)

        self.status_label = QLabel(self.last_calendar_status)
        self.status_label.setWordWrap(True)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Hora NY", "Hora local", "Moneda", "Impacto", "Evento", "Alerta"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        root.addWidget(header)
        root.addWidget(subtitle)
        root.addLayout(button_row)
        root.addWidget(self.table)

        self.setCentralWidget(central)

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #080808;
            }

            QWidget {
                background-color: #080808;
                color: #F5F1E8;
                font-family: Arial;
            }

            QLabel {
                color: #F5F1E8;
            }

            QPushButton {
                background-color: #151515;
                color: #F5F1E8;
                border: 1px solid #C9A227;
                border-radius: 8px;
                padding: 9px 14px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #C9A227;
                color: #080808;
            }

            QTableWidget {
                background-color: #101010;
                color: #F5F1E8;
                border: 1px solid #2A2A2A;
                gridline-color: #2A2A2A;
                selection-background-color: #B87333;
                selection-color: #080808;
            }

            QHeaderView::section {
                background-color: #151515;
                color: #C9A227;
                border: 1px solid #2A2A2A;
                padding: 8px;
                font-weight: 700;
            }
            """
        )

    def _update_alerts_button_style(self) -> None:
        if self.alerts_enabled:
            self.alerts_toggle_button.setText("Alertas ON")
            self.alerts_toggle_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #C9A227;
                    color: #080808;
                    border: 1px solid #C9A227;
                    border-radius: 8px;
                    padding: 9px 14px;
                    font-weight: 800;
                }

                QPushButton:hover {
                    background-color: #F5F1E8;
                    color: #080808;
                }
                """
            )
        else:
            self.alerts_toggle_button.setText("Alertas OFF")
            self.alerts_toggle_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #2A2A2A;
                    color: #8C8C8C;
                    border: 1px solid #8C8C8C;
                    border-radius: 8px;
                    padding: 9px 14px;
                    font-weight: 800;
                }

                QPushButton:hover {
                    background-color: #3A3A3A;
                    color: #F5F1E8;
                }
                """
            )

    def _refresh_status_label(self) -> None:
        alerts_state = "ON" if self.alerts_enabled else "OFF"
        self.status_label.setText(f"{self.last_calendar_status} | Alertas: {alerts_state}")

    def toggle_alerts(self, enabled: bool | None = None) -> None:
        if enabled is None:
            self.alerts_enabled = not self.alerts_enabled
        else:
            self.alerts_enabled = enabled

        self._update_alerts_button_style()
        self._update_tray_menu_state()
        self._update_tray_tooltip()

        if self.alerts_enabled:
            self._schedule_alerts()
        else:
            self._clear_alert_timers()
            self._close_active_popups()

        self._refresh_status_label()

    def refresh_calendar(self) -> None:
        self.load_forexfactory_calendar(force_refresh=False)

    def open_settings(self) -> None:
        dialog = SettingsWindow(self)

        if dialog.exec() == SettingsWindow.DialogCode.Accepted:
            self.settings = load_settings()
            self.alerted_events.clear()
            self.played_post_event_sounds.clear()
            self.load_forexfactory_calendar(force_refresh=False)

    def load_forexfactory_calendar(self, force_refresh: bool = False) -> None:
        self.status_label.setText("Consultando calendario económico...")

        try:
            result = fetch_forexfactory_events(
                timezone_name=self.settings.get("timezone", "America/Mexico_City"),
                currencies=self.settings.get(
                    "currencies",
                    ["USD", "CNY", "GBP", "JPY", "CAD", "EUR", "ALL"],
                ),
                impacts=self.settings.get("impacts", ["High", "Medium"]),
                active_start=self.settings.get("active_start", "07:00"),
                active_end=self.settings.get("active_end", "13:00"),
                force_refresh=force_refresh,
            )

        except ForexFactoryError as exc:
            self.events = []
            self._clear_alert_timers()
            self._render_events()
            self.last_calendar_status = "Error consultando ForexFactory. No hay cache disponible."
            self._refresh_status_label()
            QMessageBox.warning(self, "PIT ALERT", str(exc))
            return

        self.events = result.events
        self.alerted_events.clear()
        self.played_post_event_sounds.clear()
        self._clear_alert_timers()
        self._render_events()
        self._schedule_alerts()

        now = datetime.now(
            tz=ZoneInfo(self.settings.get("timezone", "America/Mexico_City"))
        )

        status = (
            f"Calendario cargado desde {result.source}: "
            f"{now.strftime('%Y-%m-%d %H:%M:%S')} "
            f"{self.settings.get('timezone')} | "
            f"Total semana: {result.total_received} | "
            f"Hoy: {result.today_count} | "
            f"Monedas: {result.currency_count} | "
            f"Impacto: {result.impact_count} | "
            f"Mostrados: {result.time_window_count}"
        )

        if result.cache_message:
            status += f" | {result.cache_message}"

        self.last_calendar_status = status
        self._refresh_status_label()

        if result.source == "CACHE_FALLBACK":
            QMessageBox.information(
                self,
                "PIT ALERT",
                "ForexFactory no respondió correctamente. Se usó cache local.",
            )

    def _render_events(self) -> None:
        self.table.setRowCount(len(self.events))

        alert_minutes = int(self.settings.get("alert_minutes_before", 3))

        for row, event in enumerate(self.events):
            alert_time = event.event_time - timedelta(minutes=alert_minutes)

            ny_time = event.event_time.astimezone(ZoneInfo("America/New_York"))
            values = [
                ny_time.strftime("%H:%M:%S"),
                event.event_time.strftime("%H:%M:%S"),
                event.currency,
                event.impact,
                event.title,
                alert_time.strftime("%H:%M:%S"),
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                    if col != 4
                    else Qt.AlignmentFlag.AlignLeft
                )
                self.table.setItem(row, col, item)

                if col == 3 and value in ("Medium", "High"):
                    self.table.removeCellWidget(row, col)
                    badge = self._create_impact_badge(value)
                    self.table.setCellWidget(row, col, badge)

        self.table.resizeColumnsToContents()
        self._update_row_colors()

    def _create_impact_badge(self, impact: str) -> QWidget:
        container = QWidget()
        container.setStyleSheet("background-color: transparent;")

        layout = QHBoxLayout(container)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel(impact)
        label.setObjectName("impactLabel")
        label.setFont(QFont("Arial", 9, QFont.Weight.Bold))

        if impact == "Medium":
            label.setStyleSheet("""
                QLabel {
                    background-color: #D4AF37; /* Amarillo/Dorado suave */
                    color: #FFFFFF;
                    border-radius: 4px;
                    padding: 2px 8px;
                }
            """)
        elif impact == "High":
            label.setStyleSheet("""
                QLabel {
                    background-color: #B22222; /* Rojo/Carmesí suave */
                    color: #FFFFFF;
                    border-radius: 4px;
                    padding: 2px 8px;
                }
            """)

        layout.addWidget(label)
        return container

    def _schedule_alerts(self) -> None:
        self._clear_alert_timers()

        if not self.alerts_enabled or self.is_closing:
            return

        alert_minutes = int(self.settings.get("alert_minutes_before", 3))
        now = (
            datetime.now(tz=self.events[0].event_time.tzinfo)
            if self.events
            else None
        )

        if now is None:
            return

        for event in self.events:
            event_key = self._event_key(event)
            alert_time = event.event_time - timedelta(minutes=alert_minutes)
            post_time = event.event_time + timedelta(minutes=3)

            # Schedule standard alert
            if event_key not in self.alerted_events:
                if event.event_time > now:
                    if alert_time <= now < event.event_time:
                        self._show_alert(event)
                    else:
                        delay_ms = int((alert_time - now).total_seconds() * 1000)
                        if delay_ms > 0:
                            timer = QTimer(self)
                            timer.setSingleShot(True)
                            timer.timeout.connect(partial(self._handle_alert_timer, event_key, event))
                            self.alert_timers[event_key] = timer
                            timer.start(delay_ms)

            # Schedule post-event sound
            if event_key not in self.played_post_event_sounds:
                if post_time > now:
                    delay_post_ms = int((post_time - now).total_seconds() * 1000)
                    if delay_post_ms > 0:
                        timer_post = QTimer(self)
                        timer_post.setSingleShot(True)
                        timer_post.timeout.connect(partial(self._handle_post_event_timer, event_key, event))
                        self.post_event_timers[event_key] = timer_post
                        timer_post.start(delay_post_ms)

        self._update_tray_tooltip()

    def _handle_alert_timer(self, event_key: str, event: EconomicEvent) -> None:
        timer = self.alert_timers.pop(event_key, None)

        if timer is not None:
            timer.stop()
            timer.deleteLater()

        if self.is_closing:
            return

        self._show_alert(event)

    def _handle_post_event_timer(self, event_key: str, event: EconomicEvent) -> None:
        timer = self.post_event_timers.pop(event_key, None)

        if timer is not None:
            timer.stop()
            timer.deleteLater()

        if self.is_closing:
            return

        self._play_post_event_sound(event_key)
        self._update_row_colors()

    def _play_post_event_sound(self, event_key: str) -> None:
        if not self.settings.get("sound_enabled", True) or not self.alerts_enabled:
            return

        if event_key in self.played_post_event_sounds:
            return

        self.played_post_event_sounds.add(event_key)

        base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
        sound_path = base_path / "assets" / "two_minutes__engine_fire_up_.wav"

        if not sound_path.exists():
            return

        sound_effect = QSoundEffect(self)
        sound_effect.setSource(QUrl.fromLocalFile(str(sound_path)))
        sound_effect.setLoopCount(1)
        sound_effect.setVolume(0.9)

        def handle_status_changed():
            if not sound_effect.isPlaying():
                if sound_effect in self.active_sound_effects:
                    self.active_sound_effects.remove(sound_effect)
                sound_effect.deleteLater()

        sound_effect.playingChanged.connect(handle_status_changed)
        self.active_sound_effects.append(sound_effect)
        sound_effect.play()

    def _clear_alert_timers(self) -> None:
        for timer in list(self.alert_timers.values()):
            if timer.isActive():
                timer.stop()

            timer.deleteLater()

        self.alert_timers.clear()

        for timer in list(self.post_event_timers.values()):
            if timer.isActive():
                timer.stop()

            timer.deleteLater()

        self.post_event_timers.clear()

    def _show_alert(self, event: EconomicEvent) -> None:
        if not self.alerts_enabled or self.is_closing:
            return

        event_key = self._event_key(event)

        if event_key in self.alerted_events:
            return

        now = datetime.now(tz=event.event_time.tzinfo)

        if event.event_time <= now:
            return

        self.alerted_events.add(event_key)

        self.active_popups = [popup for popup in self.active_popups if popup.isVisible()]

        popup = AlertPopup(event=event, settings=self.settings)
        self.active_popups.append(popup)
        popup.show()

    def show_test_popup(self) -> None:
        tz = ZoneInfo(self.settings.get("timezone", "America/Mexico_City"))
        event_time = datetime.now(tz=tz) + timedelta(minutes=3)
        event = EconomicEvent(
            title="Core CPI m/m (Prueba)",
            currency="USD",
            impact="High",
            event_time=event_time,
        )

        self._show_alert(event)

        # Programar Audio 2 para este evento de prueba a los 6 minutos (3 min después de la noticia)
        event_key = self._event_key(event)
        timer_post = QTimer(self)
        timer_post.setSingleShot(True)
        timer_post.timeout.connect(partial(self._handle_post_event_timer, event_key, event))
        self.post_event_timers[event_key] = timer_post
        timer_post.start(360000)

    def show_fast_popup(self) -> None:
        tz = ZoneInfo(self.settings.get("timezone", "America/Mexico_City"))

        event = EconomicEvent(
            title="Fed Chair Powell Speaks (Prueba)",
            currency="USD",
            impact="High",
            event_time=datetime.now(tz=tz) + timedelta(seconds=10),
        )

        self._show_alert(event)

        # Programar Audio 2 para este evento rápido de prueba a los 20 segundos (10s después de la noticia)
        event_key = self._event_key(event)
        timer_post = QTimer(self)
        timer_post.setSingleShot(True)
        timer_post.timeout.connect(partial(self._handle_post_event_timer, event_key, event))
        self.post_event_timers[event_key] = timer_post
        timer_post.start(20000)

    def play_test_audio2(self) -> None:
        # Reproducir Audio 2 de forma inmediata e independiente
        self._play_post_event_sound("test_audio2_manual_key")
        # Forzar que la clave manual se borre después para permitir volver a probar el botón
        self.played_post_event_sounds.discard("test_audio2_manual_key")

    def _remove_popup_reference(self, popup: AlertPopup, *args) -> None:
        if popup in self.active_popups:
            self.active_popups.remove(popup)

    def _close_active_popups(self) -> None:
        for popup in list(self.active_popups):
            popup.close()

        self.active_popups.clear()

    @staticmethod
    def _event_key(event: EconomicEvent) -> str:
        return f"{event.event_time.isoformat()}|{event.currency}|{event.title}"

    def _setup_tray_icon(self, icon_path: Path | str | None = None) -> None:
        if icon_path is None:
            base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
            icon_path = base_path / "assets" / "icons" / "pit_alert2.ico"

        icon_file = Path(icon_path)
        if not icon_file.exists():
            icon_file = Path(icon_path).with_suffix(".png")

        if icon_file.exists():
            self.tray_icon_obj = QIcon(str(icon_file))
        else:
            self.tray_icon_obj = self.windowIcon() if not self.windowIcon().isNull() else QIcon()

        self.tray_icon = QSystemTrayIcon(self.tray_icon_obj, self)
        self._update_tray_tooltip()

        self.tray_menu = QMenu(self)

        self.action_abrir = QAction("Abrir PIT ALERT", self)
        self.action_abrir.triggered.connect(self.restore_from_tray)

        self.action_alertas = QAction("Alertas ON/OFF", self)
        self.action_alertas.setCheckable(True)
        self.action_alertas.setChecked(self.alerts_enabled)
        self.action_alertas.toggled.connect(self.on_tray_alertas_toggled)

        self.action_cerrar = QAction("Cerrar definitivamente", self)
        self.action_cerrar.triggered.connect(self.quit_app)

        self.tray_menu.addAction(self.action_abrir)
        self.tray_menu.addAction(self.action_alertas)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.action_cerrar)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon.show()

    def on_tray_alertas_toggled(self, checked: bool) -> None:
        if checked != self.alerts_enabled:
            self.toggle_alerts(checked)

    def _update_tray_menu_state(self) -> None:
        if hasattr(self, "action_alertas"):
            self.action_alertas.blockSignals(True)
            self.action_alertas.setChecked(self.alerts_enabled)
            self.action_alertas.blockSignals(False)

    def _update_tray_tooltip(self) -> None:
        if not hasattr(self, "tray_icon"):
            return

        if not self.alerts_enabled:
            self.tray_icon.setToolTip("🔴 PIT ALERT: Alertas PAUSADAS")
            return

        next_event = None
        if self.events:
            now = datetime.now(tz=self.events[0].event_time.tzinfo)
            future_events = [e for e in self.events if e.event_time > now]
            if future_events:
                next_event = min(future_events, key=lambda e: e.event_time)

        if next_event:
            now = datetime.now(tz=next_event.event_time.tzinfo)
            mins_left = max(0, int((next_event.event_time - now).total_seconds() // 60))
            tooltip = (
                f"🟢 PIT ALERT: Alertas ACTIVAS\n"
                f"Próximo: {next_event.currency} - {next_event.title} (en {mins_left} min)"
            )
        else:
            tooltip = "🟢 PIT ALERT: Alertas ACTIVAS\nSin eventos pendientes hoy"

        self.tray_icon.setToolTip(tooltip)
        self._update_row_colors()

    def _update_row_colors(self) -> None:
        if not self.events:
            return

        now = datetime.now(tz=self.events[0].event_time.tzinfo)
        gray_color = QColor("#8C8C8C")
        default_color = QColor("#F5F1E8")

        for row, event in enumerate(self.events):
            post_time = event.event_time + timedelta(minutes=3)
            is_past = now >= post_time

            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item is not None:
                    item.setForeground(gray_color if is_past else default_color)

            # Actualizar el color del badge de impacto si existe en la columna 3
            widget = self.table.cellWidget(row, 3)
            if widget is not None:
                label = widget.findChild(QLabel, "impactLabel")
                if label is not None:
                    impact = label.text()
                    if is_past:
                        label.setStyleSheet("""
                            QLabel {
                                background-color: #2A2A2A;
                                color: #8C8C8C;
                                border-radius: 4px;
                                padding: 2px 8px;
                            }
                        """)
                    else:
                        if impact == "Medium":
                            label.setStyleSheet("""
                                QLabel {
                                    background-color: #D4AF37;
                                    color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 2px 8px;
                                }
                            """)
                        elif impact == "High":
                            label.setStyleSheet("""
                                QLabel {
                                    background-color: #B22222;
                                    color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 2px 8px;
                                }
                            """)

    def on_tray_icon_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (QSystemTrayIcon.ActivationReason.Trigger, QSystemTrayIcon.ActivationReason.DoubleClick):
            if self.isHidden() or self.isMinimized():
                self.restore_from_tray()
            else:
                self.hide()

    def restore_from_tray(self) -> None:
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def quit_app(self) -> None:
        self.is_closing = True
        self._clear_alert_timers()
        self._close_active_popups()
        if hasattr(self, "tray_icon"):
            self.tray_icon.hide()
        QApplication.instance().quit()

    def closeEvent(self, event) -> None:
        if self.is_closing:
            self._clear_alert_timers()
            self._close_active_popups()
            if hasattr(self, "tray_icon"):
                self.tray_icon.hide()
            event.accept()
        else:
            event.ignore()
            self.hide()
            if not self.has_shown_tray_message and hasattr(self, "tray_icon"):
                self.has_shown_tray_message = True
                if self.tray_icon.supportsMessages():
                    self.tray_icon.showMessage(
                        "PIT ALERT",
                        "La aplicación sigue ejecutándose en segundo plano.",
                        QSystemTrayIcon.MessageIcon.Information,
                        3000,
                    )