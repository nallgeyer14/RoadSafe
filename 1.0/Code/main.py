import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from OBD import OBDAdapter
from sim import NormalSimulator
from analyzer import Analyzer
from PySide6.QtCore import QTimer
from ui import Dashboard



app = QApplication(sys.argv)

window = Dashboard()
window.show()

analyzer = Analyzer()
obd = OBDAdapter()
sim = NormalSimulator()

speed_history =[]
rpm_history = []
time_history = []


def update_vehicle():
    
    
    print("timer running")
    reading = sim.get_reading()

    print(reading)

   
    time_history.append(len(time_history))
    speed_history.append(reading.speed)
    rpm_history.append(reading.rpm)

    window.update_dashboard(
        reading
    )
    alerts = analyzer.check(reading)

    if alerts:
        print(alerts)

timer = QTimer()
timer.timeout.connect(update_vehicle)
timer.start(100)


sys.exit(app.exec())