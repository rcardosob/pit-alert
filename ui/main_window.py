from __future__ import annotations

from datetime import datetime, timedelta
from functools import partial
from zoneinfo import ZoneInfo

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)

from core.event_model import EconomicEvent
from core.settings import load_settings
from sources.forexfactory import fetch_forexfactory_events, ForexFactoryError
from ui.alert_popup import AlertPopup
from ui.settings_window import SettingsWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.settings = load_settings()
        self.events: list[EconomicEvent] = []
        self.alerted_events: set[str] = set()
        self.active_popups: list[AlertPopup] = []
        self.alert_timers: dict[str, QTimer] = {}

        self.alerts_enabled = True
        self.is_closing = False
        self.last_calendar_status = "Calendario no cargado."

        self.setWindowTitle("PIT ALERT")
        self.resize(980, 620)

        self._build_ui()
        self._apply_styles()
        self._update_alerts_button_style()

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

            button_row.addWidget(self.test_popup_button)
            button_row.addWidget(self.fast_popup_button)

        button_row.addStretch(1)

        self.status_label = QLabel(self.last_calendar_status)
        self.status_label.setWordWrap(True)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Hora local", "Moneda", "Impacto", "Evento", "Alerta"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        root.addWidget(header)
        root.addWidget(subtitle)
        root.addLayout(button_row)
        root.addWidget(self.status_label)
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

    def toggle_alerts(self) -> None:
        self.alerts_enabled = not self.alerts_enabled
        self._update_alerts_button_style()

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

            values = [
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
                    if col != 3
                    else Qt.AlignmentFlag.AlignLeft
                )
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()

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

            if event_key in self.alerted_events:
                continue

            if event.event_time <= now:
                continue

            if alert_time <= now < event.event_time:
                self._show_alert(event)
                continue

            delay_ms = int((alert_time - now).total_seconds() * 1000)

            if delay_ms > 0:
                timer = QTimer(self)
                timer.setSingleShot(True)
                timer.timeout.connect(partial(self._handle_alert_timer, event_key, event))
                self.alert_timers[event_key] = timer
                timer.start(delay_ms)

    def _handle_alert_timer(self, event_key: str, event: EconomicEvent) -> None:
        timer = self.alert_timers.pop(event_key, None)

        if timer is not None:
            timer.stop()
            timer.deleteLater()

        if self.is_closing:
            return

        self._show_alert(event)

    def _clear_alert_timers(self) -> None:
        for timer in list(self.alert_timers.values()):
            if timer.isActive():
                timer.stop()

            timer.deleteLater()

        self.alert_timers.clear()

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

        event = EconomicEvent(
            title="Core CPI m/m",
            currency="USD",
            impact="High",
            event_time=datetime.now(tz=tz) + timedelta(minutes=3),
        )

        self._show_alert(event)

    def show_fast_popup(self) -> None:
        tz = ZoneInfo(self.settings.get("timezone", "America/Mexico_City"))

        event = EconomicEvent(
            title="Fed Chair Powell Speaks",
            currency="USD",
            impact="High",
            event_time=datetime.now(tz=tz) + timedelta(seconds=10),
        )

        self._show_alert(event)

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

    def closeEvent(self, event) -> None:
        self.is_closing = True
        self._clear_alert_timers()
        self._close_active_popups()
        event.accept()