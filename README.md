# RoadSafe

RoadSafe is a Python-based vehicle monitoring and diagnostic simulator designed to emulate real-time OBD-II vehicle telemetry. The project began as a simple sensor simulator but has evolved into a stateful vehicle model capable of generating realistic driving behavior, detecting abnormal conditions, and preparing for integration with real OBD-II hardware.

The long-term goal is to create a diagnostic engine capable of monitoring live vehicle data, identifying potential mechanical issues, and providing meaningful alerts rather than simply displaying raw sensor values.

---

## Features

### Vehicle Simulation

* Stateful driving simulation
* Idle, Accelerating, Cruise, and Decelerating driving states
* Automatic gear shifting
* Realistic acceleration and drag
* Dynamic RPM based on speed and gear ratio
* Simulated engine coolant temperature
* Continuous telemetry generation

### Telemetry

Each generated reading includes:

* Timestamp
* Vehicle speed (MPH)
* Engine RPM
* Throttle position (%)
* Coolant temperature (°F)
* Current driving state
* Current gear

### Vehicle Analyzer

The analyzer processes telemetry and generates alerts for abnormal behavior.

Current detections include:

* Rapid acceleration
* Sudden speed spikes
* Vehicle moving while in Idle state
* High coolant temperature
* Custom rule-based alerts

The analyzer is designed so new diagnostic rules can be added with minimal changes.

---

## Project Structure

```
RoadSafe/
│
├── main.py              # Program entry point
├── sim.py               # Vehicle simulation engine
├── analyzer.py          # Alert detection logic
├── models.py            # VehicleReading dataclass
└── README.md
```

---

## How It Works

1. The simulator generates realistic vehicle telemetry.
2. Telemetry is stored as a `VehicleReading`.
3. The analyzer evaluates each reading.
4. Alerts are generated if abnormal conditions are detected.
5. Results are displayed in real time.

Example output:

```
Timestamp: 2026-07-02 22:57:31

Speed: 57.7 MPH
RPM: 2755
Throttle: 12%
Coolant Temp: 160°F
State: Cruise
Gear: 4

No alerts detected.
```

---

## Current Vehicle Model

The simulator currently models:

* Idle engine behavior
* Smooth acceleration
* Cruise control behavior
* Vehicle deceleration
* Gear shifting
* RPM changes
* Coolant temperature changes
* Vehicle drag

Rather than generating completely random values, each reading depends on the previous reading, producing realistic transitions between driving conditions.

---

## Future Plans

RoadSafe is intended to become a real-time diagnostic assistant rather than simply an OBD-II dashboard.

Planned features include:

* Live OBD-II integration using an ELM327 adapter
* Support for python-OBD
* Historical trend analysis
* Trip statistics
* Fault confidence scoring
* Intelligent diagnostic recommendations
* Sensor anomaly detection
* Transmission slip detection
* Engine overheating prediction
* Aggressive driving analysis
* Data logging to CSV or SQLite
* Live dashboard interface
* Graphing of sensor data
* Configurable alert thresholds

---

## Technologies Used

* Python 3
* Dataclasses
* Object-Oriented Programming
* Random-based state simulation
* Rule-based anomaly detection

---

## Why This Project?

Most consumer OBD-II applications simply display vehicle information.

RoadSafe aims to go one step further by interpreting vehicle telemetry and identifying meaningful patterns that may indicate unsafe driving conditions or developing mechanical issues.

The project is also designed so the same analysis engine can work with either:

* Simulated vehicle data (development and testing)
* Real OBD-II telemetry (future implementation)

This allows diagnostic rules to be developed and tested without requiring constant access to a physical vehicle.

---

## Future Hardware Integration

The planned hardware setup is:

```
Vehicle
    │
OBD-II Port
    │
ELM327 Adapter
    │
python-OBD
    │
VehicleReading
    │
RoadSafe Analyzer
    │
Warnings & Alerts
```

No major changes to the analyzer should be required when transitioning from simulated data to live vehicle telemetry.

---

## License

This project is intended for educational and personal development purposes.
