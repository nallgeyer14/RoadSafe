from dataclasses import dataclass
from datetime import datetime

@dataclass
class VehicleReading:
    timestamp: datetime
    speed: int  # in MPH
    rpm: int  # in revolutions per minute
    throttle: int # in percentage
    coolant_temp: int  # in degrees Fahrenheit
    state : str
    spike : bool
    gear: int