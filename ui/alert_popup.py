from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QTimer, QPoint, QUrl
from PySide6.QtGui import QFont, QMouseEvent, QCloseEvent
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy,
)

from core.event_model import EconomicEvent


BASE_DIR = Path(__file__).resolve().parent.parent
SOUND_PATH = BASE_DIR / "assets" / "pit_stop.wav"


class AlertPopup(QWidget):
    def __init__(
        self,
        event: EconomicEvent,
        settings: dict,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.economic_event = event
        self.settings = settings
        self.drag_position: QPoint | None = None
        self.sound: QSoundEffect | None = None

        self.setWindowTitle("PIT ALERT")
        self.setFixedSize(
            int(settings.get("popup_width", 520)),
            int(settings.get("popup_height", 300)),
        )

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._build_ui()
        self._play_sound_once()

        self.timer = QTimer(self)
        self.timer.setInterval(16)
        self.timer.timeout.connect(self._update_countdown)
        self.timer.start()

        self._update_countdown()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.frame = QFrame()
        self.frame.setObjectName("alertFrame")
        self.frame.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.frame.setStyleSheet(
            """
            QFrame#alertFrame {
                background-color: #080808;
                border: 2px solid #C9A227;
                border-radius: 18px;
            }

            QLabel#titleLabel {
                color: #C9A227;
                font-weight: 700;
                letter-spacing: 3px;
            }

            QLabel#timerLabel {
                color: #F5F1E8;
                font-weight: 800;
            }

            QLabel#eventLabel {
                color: #F5F1E8;
                font-weight: 500;
            }

            QPushButton#closeButton {
                background-color: #151515;
                color: #F5F1E8;
                border: 1px solid #B87333;
                border-radius: 8px;
                padding: 8px 18px;
                font-weight: 600;
            }

            QPushButton#closeButton:hover {
                background-color: #B87333;
                color: #080808;
            }
            """
        )

        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(28, 22, 28, 22)
        layout.setSpacing(14)

        self.title_label = QLabel("PIT ALERT")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 18))

        self.timer_label = QLabel("03:00.000")
        self.timer_label.setObjectName("timerLabel")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 58))

        self.event_label = QLabel(self.economic_event.display_title)
        self.event_label.setObjectName("eventLabel")
        self.event_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.event_label.setWordWrap(True)
        self.event_label.setFont(QFont("Arial", 15))

        self.close_button = QPushButton("Cerrar")
        self.close_button.setObjectName("closeButton")
        self.close_button.clicked.connect(self.close)

        layout.addWidget(self.title_label)
        layout.addStretch(1)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.event_label)
        layout.addStretch(1)
        layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignCenter)

        root.addWidget(self.frame)

    def _play_sound_once(self) -> None:
        if not self.settings.get("sound_enabled", True):
            return

        if not SOUND_PATH.exists():
            return

        self.sound = QSoundEffect(self)
        self.sound.setSource(QUrl.fromLocalFile(str(SOUND_PATH)))
        self.sound.setLoopCount(1)
        self.sound.setVolume(0.9)
        self.sound.play()

    def _update_countdown(self) -> None:
        now = datetime.now(tz=self.economic_event.event_time.tzinfo)
        remaining = self.economic_event.event_time - now
        remaining_ms = int(remaining.total_seconds() * 1000)

        if remaining_ms <= 0:
            self.timer_label.setText("00:00.000")

            if self.settings.get("auto_close_at_zero", True):
                self.close()

            return

        minutes = remaining_ms // 60_000
        seconds = (remaining_ms % 60_000) // 1000
        milliseconds = remaining_ms % 1000

        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}")

        if remaining_ms <= 60_000:
            self.timer_label.setStyleSheet("color: #B87333; font-weight: 800;")
        else:
            self.timer_label.setStyleSheet("color: #F5F1E8; font-weight: 800;")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.drag_position = None
        event.accept()

    def closeEvent(self, event: QCloseEvent) -> None:
        if hasattr(self, "timer") and self.timer.isActive():
            self.timer.stop()

        event.accept()