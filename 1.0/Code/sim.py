# This program is a simulation of a cars OBD2 reader. It will read data from a car's OBD2 port and display it on the screen. The program will also allow the user to send commands to the car's OBD2 system and receive responses. 

import random
from datetime import datetime
from models import VehicleReading
import time
from collections import deque


class Simulator:
    def get_reading(self):
        rpm = random.randint(500, 7000)  # Simulate RPM between 500 and 7000p
        speed = random.randint(0, 120)  # Simulate speed between 0 and 120 MPH
        throttle = random.randint(0, 100)  # Simulate throttle position
        coolant_temp = random.randint(160, 250)  # Simulate coolant temperature between 160 and 250°F

        #occasonally simulate a spike in one of the variables above to test the analyzer
        if random.random() < 0.1:  # 10% chance to spike
            rpm = random.randint(7000, 10000)  # Spike RPM
        if random.random() < 0.1:  # 10% chance to spike
            speed = random.randint(120, 200)  # Spike speed
        if random.random() < 0.1:  # 10% chance to spike
            throttle = random.randint(100, 150)  # Spike throttle
        if random.random() < 0.1:  # 10% chance to spike
            coolant_temp = random.randint(250, 300)  # Spike coolant temperature

        return VehicleReading(
            timestamp=datetime.now(),
            speed=speed,
            rpm=rpm,
            throttle=throttle,
            coolant_temp=coolant_temp
            )  
    

class NormalSimulator:

    
    def  __init__(self):
        self.state = "Idle"  # Initial state
        self.speed = 0
        self.acceleration = 0
        self.throttle = 0
        self.coolant_temp = 180  # Normal operating temperature
        self.gear = 1
        self.target_speed = 60
        self.rpm_history = deque(maxlen=100)
        self.speed_history = deque(maxlen=100)
        self.throttle_history = deque(maxlen=100)
        self.temp_history = deque(maxlen=100)
        
        self.gear_ratios = {
            1: 95,
            2: 65,
            3: 48,
            4: 36,
            5: 28,
            6: 22
        }

        self.max_speed_per_gear = {
            1: 20,
            2: 35,
            3: 55,
            4: 75,
            5: 95,
            6: 140 
        }
        self.shift_timer = 0
        self.rpm = 750
        self.last_time = time.time()
       
       
        self.spike_chance = 0.00001 # 1% chance to inject a spike

    def _inject_spike(self, reading):
        return random.random() < self.spike_chance # 5% chance to inject a spike
        

    def _apply_spike(self):
      return {
        "rpm_boost": random.randint(2000, 5000),
        "speed_boost": random.randint(20, 80),
        "throttle_override": 100,
        }
  
    # Transition betwfeen states based on current conditions

    def _transition(self):
        # Randomly transition between states
        if self.state == "Idle":
            if random.random() < 0.25:
                self.state = "Accelerating"
            return
        
        if self.state == "Accelerating":
           if self.speed > 55:
                self.state = "Cruise"
           elif self.throttle <= 2:
               self.state = "Decelerating"

        elif self.state == "Cruise":
           
           throttle_noise = random.uniform(-4,4)
           effective_throttle = self.throttle + throttle_noise
           
           if effective_throttle > 25:
                self.state = "Accelerating"

           elif effective_throttle < 8:
                self.state = "Decelerating"
       
        elif self.state == "Decelerating":
            if  self.speed < 2:
                self.state = "Idle"

    def _shift_gear(self, dt):
        self.shift_timer += dt
        
        if self.shift_timer < 2:
            return # Only shift gears every 2 readings to avoid rapid gear changes
        
        if self.speed > self.max_speed_per_gear[self.gear] and self.gear < 6:
            self.gear += 1
            self.rpm *= 0.72
            self.shift_timer = 0
            
        elif self.gear > 1 and self.speed < self.max_speed_per_gear[self.gear-1] - 5:
            self.gear -= 1
            self.rpm*=1.35
            self.shift_timer = 0

    def get_reading(self):
       
          # Update the state based on current conditions
        # Target speed for cruising
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        spike = self._inject_spike(None)  # Determine if a spike should be injected
        
       
        spike_data = self._apply_spike() if spike else None  # Apply spike if needed

        # Generate readings based on the current state
      
        if self.state == "Idle":
            self.throttle = random.randint (0, 3)  # Low throttle
            self.acceleration = 0
            self.speed *= 0.90 
            self.rpm = 700 + random.randint (-20, 20)
     
        elif self.state == "Accelerating":
            self.throttle = random.randint(20, 70)  # Moderate throttle
            
            target_acceleration = self.throttle / 18
            self.acceleration += (target_acceleration - self.acceleration) * 0.25 # Increase acceleration based on throttle
   
        elif self.state == "Cruise":
            self.throttle = random.randint(10, 20)  # Low to moderate throttle
            self.acceleration = (self.target_speed - self.speed) * 0.03  # Adjust acceleration to maintain target speed
      
        elif self.state == "Decelerating":
            self.throttle = random.uniform (0,10)  # Low throttle
            self.acceleration = max(self.acceleration - random.uniform (0.5, 1.5), -3)
         
       
        #apply physics
        self.speed += self.acceleration * dt  # Update speed based on acceleration
        self.speed *= (0.998 ** dt) # Gradually decrease speed due to drag
        self.speed = max(0, round(self.speed, 1))  # Ensure speed doesn't go below 0 and round to 1 decimal place
       

        if spike:
            self.rpm += spike_data["rpm_boost"]
            self.speed += spike_data["speed_boost"]
            self.throttle = spike_data["throttle_override"]
            self.acceleration = max(self.acceleration, 5)

        

        target_rpm = 700 + (self.speed * self.gear_ratios[self.gear])  # Simple formula to relate speed to RPM
       
        self.rpm += (target_rpm - self.rpm) * 0.1  # Smoothly adjust RPM towards target
        self.rpm = max(650, int(self.rpm))  # Ensure RPM doesn't go below idle
        self.rpm = int(self.rpm)  # Ensure RPM is an integer

        self._shift_gear(dt)  # Shift gears based on RPM

        if self.rpm > 3200:
            self.coolant_temp += 0.15 * dt
        else:
            self.coolant_temp -= 0.3 * dt
        
        self.coolant_temp = max(160, min(250, self.coolant_temp))  # Keep coolant temp within realistic bounds
       
        self.rpm_history.append(self.rpm)
        self.speed_history.append(self.speed)
        self.throttle_history.append(self.throttle)
        self.temp_history.append(self.coolant_temp)

        self._transition()
        return VehicleReading (
            timestamp=datetime.now(),
            speed=self.speed,
            rpm=self.rpm,
            throttle=self.throttle,
            coolant_temp=round(self.coolant_temp, 1),
            state=self.state,
            spike=spike,
            gear=self.gear
            )



class SportSimulator:
    def get_reading(self):

           
        rpm = random.randint(500, 8000)  # Simulate RPM between 500 and 8000
        speed = random.randint(0, 150)  # Simulate speed between 0 and 150 MPH
        throttle = random.randint(0, 100)  # Simulate throttle position
        coolant_temp = random.randint(160, 250)  # Simulate coolant temperature between 160 and 250°F

        return VehicleReading(
            timestamp=datetime.now(),
            speed=speed,
            rpm=rpm,
            throttle=throttle,
            coolant_temp=coolant_temp
            )
        


SIMULATORS = {
    "normal": NormalSimulator,
    "sport": SportSimulator
}