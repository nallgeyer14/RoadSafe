import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel, 
    QMainWindow,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout
)
from widgets.gauge import Gauge
from widgets.graph import VehicleGraph


class Dashboard(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("RoadSafe")
        self.resize(1000,700)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        title = QLabel("RoadSafe Vehicle Monitor")
        title.setStyleSheet("font-size:24px;font-weight:bold;")

        self.speed = QLabel("Speed: 0 MPH")
        self.rpm = QLabel("RPM: 0")
        self.gear = QLabel("Gear 1")
        self.state = QLabel("State: Idle")
        self.throttle= QLabel("Throttle: 0%")
        self.coolant = QLabel("Temp: 180°F")

        

        layout.addWidget(title)
        

        gauge_layout = QHBoxLayout()

        self.speed_gauge = Gauge(
            "Speed MPH",
            0,
            160
        )
        self.rpm_gauge = Gauge(
            "RPM",
            0,
            9000
        )
        gauge_layout.addWidget(self.speed_gauge)
        gauge_layout.addWidget(self.rpm_gauge)

        layout.addLayout(gauge_layout)
    def update_dashboard(self,reading):

        self.speed_gauge.update_value(
            reading.speed
        )

        self.rpm_gauge.update_value(
            reading.rpm
        )


        self.speed.setText(
            f"Speed: {reading.speed:.0f} MPH"
        )

        self.rpm.setText(
            f"RPM: {reading.rpm:.0f}"
        )
        self.throttle.setText(
        f"Throttle: {reading.throttle:.0f}%"
    )

        self.coolant.setText(
        f"Coolant: {reading.coolant_temp:.0f}°F"
    )
