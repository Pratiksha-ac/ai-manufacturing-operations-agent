import json
from database import insert_telemetry


def process_telemetry(message):
    try:
        telemetry = json.loads(message)

        required_fields = [
            "machine_id",
            "timestamp",
            "temperature",
            "vibration",
            "pressure",
            "rpm",
            "energy_consumption",
            "status"
        ]

        for field in required_fields:
            if field not in telemetry:
                print(f"Missing field: {field}")
                return None

        print("Telemetry processed successfully")
        print(f"Machine ID: {telemetry['machine_id']}")
        print(f"Temperature: {telemetry['temperature']}")
        print(f"Vibration: {telemetry['vibration']}")
        print(f"Pressure: {telemetry['pressure']}")
        print(f"RPM: {telemetry['rpm']}")
        print(f"Energy: {telemetry['energy_consumption']}")
        print(f"Status: {telemetry['status']}")

        insert_telemetry(telemetry)

        return telemetry

    except json.JSONDecodeError:
        print("Invalid JSON received")
        return None