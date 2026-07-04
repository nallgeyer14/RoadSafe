import time 
import dashboard
import matplotlib.pyplot as plt

from OBD import OBDAdapter
from sim import NormalSimulator
from analyzer import Analyzer
from dashboard import update_dashboard

analyzer = Analyzer()
obd = OBDAdapter()
sim = NormalSimulator()

speed_history =[]
rpm_history = []
time_history = []


while True:
    reading = sim.get_reading()

    time_history.append(len(time_history))
    speed_history.append(reading.speed)
    rpm_history.append(reading.rpm)

    update_dashboard(time_history, speed_history, rpm_history)
    
    print(reading)  
    alerts = analyzer.check(reading)
    
    print("\n--- Vehicle Reading ---")
    print(f"Timestamp: {reading.timestamp}, \nSpeed: {reading.speed} MPH, \nRPM: {reading.rpm}, \nThrottle: {reading.throttle}%, \nCoolant Temp: {reading.coolant_temp}°F")

    if alerts:
        print ("\n--- Alerts ---")
        for alert in alerts:
            print(alert)
    else:
        print("\nNo alerts detected.")
    
    time.sleep(1)  # Wait for 1 second before getting the next reading