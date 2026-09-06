import random
import time
from datetime import datetime, timezone

class Machine:
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.temperature = 70.0
        self.vibration = 2.0
        self.pressure = 100.0
        self.rpm = 3000
        self.energy_consumption = 8.0
        self.status = "RUNNING"
        self.anomaly = False

    def update_sensors(self):
     if self.anomaly:
        self.temperature += random.uniform(1.0, 3.0)
        self.vibration += random.uniform(0.5, 1.5)
        self.pressure += random.uniform(2.0, 5.0)
        self.rpm += random.randint(-100, 100)
        self.energy_consumption += random.uniform(0.3, 0.8)
        self.status = "WARNING"

     else:
        self.temperature += random.uniform(-0.5, 0.5)
        self.vibration += random.uniform(-0.2, 0.2)
        self.pressure += random.uniform(-1.0, 1.0)
        self.rpm += random.randint(-50, 50)
        self.energy_consumption += random.uniform(-0.3, 0.3)

    def get_telemetry(self):
     return {
        "machine_id": self.machine_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": self.temperature,
        "vibration": self.vibration,
        "pressure": self.pressure,
        "rpm": self.rpm,
        "energy_consumption": self.energy_consumption,
        "status": self.status
    }

machines = [
    Machine("CNC-01"),
    Machine("CNC-02"),
    Machine("CNC-03"),
    Machine("CNC-04")
]

machines[3].anomaly = True

for i in range(10):
    for machine in machines:
        machine.update_sensors()

        telemetry = machine.get_telemetry()

        print(telemetry)

    time.sleep(1)