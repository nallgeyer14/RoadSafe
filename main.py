import time 
from sim import NormalSimulator
from OBD import OBDAdapter
from analyzer import Analyzer

sim = NormalSimulator
analyzer = Analyzer()
obd = OBDAdapter
while True:
    reading = sim.get_reading()
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
