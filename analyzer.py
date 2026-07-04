class Analyzer:

    def __init__(self):
        self.history = []  # Store the last 10 readings
    
    def update(self, reading):
        self.history.append(reading)

        if len(self.history) > 10:
            self.history.pop(0)  # Keep only the last 10 readings


    def check(self,reading):
        alerts = []

        self.update(reading)

        if len(self.history) < 3:
            return alerts  # Not enough data to analyze
        
        latest = self.history[-1]
        previous = self.history[-2]

        speeds = [r.speed for r in self.history]
        if max(speeds) - min(speeds) > 50:
            alerts.append("Alert: Sudden speed spike detected!")
        
        if latest.speed < 10 and latest.rpm > 3000:
            alerts.append("Alert: Possible engine stall detected!")

        accel = latest.speed - previous.speed
        if accel > 30:
            alerts.append("Alert: Rapid acceleration detected!")
        
        if latest.coolant_temp > 250:
            alerts.append("Alert: Coolant temperature spike detected!")
        
        spike_count = sum(1 for r in self.history[-5:] if r.spike)
        if spike_count >= 32:
            alerts.append("Alert: Multiple spikes detected in the last 5 readings!")

        if latest.state == "Idle" and latest.speed > 2:
            alerts.append("Alert: Vehicle is moving while in Idle state!")
       
        return alerts