from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QGridLayout,
    QCheckBox,
    QLabel,
    QPushButton,
    QSpinBox,
    QLineEdit,
    QMessageBox,
)

from core.settings import load_settings, save_settings


AVAILABLE_CURRENCIES = [
    "ALL",
    "USD",
    "EUR",
    "CAD",
    "CNY",
    "GBP",
    "JPY",
    "AUD",
    "CHF",
]

AVAILABLE_IMPACTS = [
    "High",
    "Medium",
    "Low",
    "Holiday",
]


class SettingsWindow(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.settings = load_settings()
        self.currency_checks: dict[str, QCheckBox] = {}
        self.impact_checks: dict[str, QCheckBox] = {}

        self.setWindowTitle("Configuración - PIT ALERT")
        self.setFixedSize(520, 560)

        self._build_ui()
        self._apply_styles()
        self._load_current_values()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        title = QLabel("Configuración")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        timezone_label = QLabel("Zona horaria local")
        self.timezone_input = QLineEdit()
        self.timezone_input.setPlaceholderText("America/Mexico_City")

        self.alert_minutes_input = QSpinBox()
        self.alert_minutes_input.setMinimum(1)
        self.alert_minutes_input.setMaximum(60)
        self.alert_minutes_input.setSuffix(" min")

        self.sound_checkbox = QCheckBox("Sonido activado")
        self.start_minimized_checkbox = QCheckBox("Iniciar minimizado en System Tray")

        general_group = QGroupBox("General")
        general_layout = QGridLayout(general_group)
        general_layout.addWidget(timezone_label, 0, 0)
        general_layout.addWidget(self.timezone_input, 0, 1)
        general_layout.addWidget(QLabel("Alerta antes del evento"), 1, 0)
        general_layout.addWidget(self.alert_minutes_input, 1, 1)
        general_layout.addWidget(self.sound_checkbox, 2, 0)
        general_layout.addWidget(self.start_minimized_checkbox, 2, 1)

        currencies_group = QGroupBox("Monedas")
        currencies_layout = QGridLayout(currencies_group)

        for index, currency in enumerate(AVAILABLE_CURRENCIES):
            checkbox = QCheckBox(currency)
            self.currency_checks[currency] = checkbox
            row = index // 3
            col = index % 3
            currencies_layout.addWidget(checkbox, row, col)

        impacts_group = QGroupBox("Impacto")
        impacts_layout = QGridLayout(impacts_group)

        for index, impact in enumerate(AVAILABLE_IMPACTS):
            checkbox = QCheckBox(impact)
            self.impact_checks[impact] = checkbox
            row = index // 2
            col = index % 2
            impacts_layout.addWidget(checkbox, row, col)

        button_row = QHBoxLayout()

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)

        self.save_button = QPushButton("Guardar cambios")
        self.save_button.clicked.connect(self._save)

        button_row.addStretch(1)
        button_row.addWidget(self.cancel_button)
        button_row.addWidget(self.save_button)

        root.addWidget(title)
        root.addWidget(general_group)
        root.addWidget(currencies_group)
        root.addWidget(impacts_group)
        root.addStretch(1)
        root.addLayout(button_row)

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QDialog {
                background-color: #080808;
                color: #F5F1E8;
                font-family: Arial;
            }

            QLabel {
                color: #F5F1E8;
            }

            QLabel#titleLabel {
                color: #C9A227;
                font-size: 24px;
                font-weight: 800;
            }

            QGroupBox {
                color: #C9A227;
                border: 1px solid #2A2A2A;
                border-radius: 10px;
                margin-top: 12px;
                padding: 14px;
                font-weight: 700;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 14px;
                padding: 0 6px;
            }

            QCheckBox {
                color: #F5F1E8;
                spacing: 8px;
                font-weight: 500;
            }

            QLineEdit, QSpinBox {
                background-color: #151515;
                color: #F5F1E8;
                border: 1px solid #C9A227;
                border-radius: 8px;
                padding: 7px;
            }

            QPushButton {
                background-color: #151515;
                color: #F5F1E8;
                border: 1px solid #C9A227;
                border-radius: 8px;
                padding: 9px 14px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #C9A227;
                color: #080808;
            }
            """
        )

    def _load_current_values(self) -> None:
        self.timezone_input.setText(
            self.settings.get("timezone", "America/Mexico_City")
        )

        self.alert_minutes_input.setValue(
            int(self.settings.get("alert_minutes_before", 3))
        )

        self.sound_checkbox.setChecked(
            bool(self.settings.get("sound_enabled", True))
        )

        self.start_minimized_checkbox.setChecked(
            bool(self.settings.get("start_minimized", False))
        )

        selected_currencies = {
            currency.upper()
            for currency in self.settings.get(
                "currencies",
                ["USD", "CNY", "GBP", "JPY", "CAD", "EUR", "ALL"],
            )
        }

        for currency, checkbox in self.currency_checks.items():
            checkbox.setChecked(currency.upper() in selected_currencies)

        selected_impacts = {
            str(impact).capitalize()
            for impact in self.settings.get("impacts", ["High", "Medium"])
        }

        for impact, checkbox in self.impact_checks.items():
            checkbox.setChecked(impact in selected_impacts)

    def _save(self) -> None:
        selected_currencies = [
            currency
            for currency, checkbox in self.currency_checks.items()
            if checkbox.isChecked()
        ]

        selected_impacts = [
            impact
            for impact, checkbox in self.impact_checks.items()
            if checkbox.isChecked()
        ]

        if not selected_currencies:
            QMessageBox.warning(
                self,
                "PIT ALERT",
                "Selecciona al menos una moneda.",
            )
            return

        if not selected_impacts:
            QMessageBox.warning(
                self,
                "PIT ALERT",
                "Selecciona al menos un nivel de impacto.",
            )
            return

        updated_settings = self.settings.copy()
        updated_settings["timezone"] = self.timezone_input.text().strip() or "America/Mexico_City"
        updated_settings["alert_minutes_before"] = int(self.alert_minutes_input.value())
        updated_settings["sound_enabled"] = self.sound_checkbox.isChecked()
        updated_settings["start_minimized"] = self.start_minimized_checkbox.isChecked()
        updated_settings["currencies"] = selected_currencies
        updated_settings["impacts"] = selected_impacts

        save_settings(updated_settings)

        self.settings = updated_settings
        self.accept()