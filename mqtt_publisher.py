import json
import time
import paho.mqtt.client as mqtt

from machine import machines


BROKER = "localhost"
PORT = 1883


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(BROKER, PORT)

client.loop_start()


try:
    while True:
        for machine in machines:

            machine.update_sensors()

            telemetry = machine.get_telemetry()

            message = json.dumps(telemetry)

            topic = f"factory/{machine.machine_id}/telemetry"

            client.publish(topic, message)

            print(f"Published to {topic}")
            print(message)
            print("-" * 50)

        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping publisher...")

finally:
    client.loop_stop()
    client.disconnect()