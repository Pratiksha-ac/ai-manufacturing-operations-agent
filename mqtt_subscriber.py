import paho.mqtt.client as mqtt
from telemetry_processor import process_telemetry


BROKER = "localhost"
PORT = 1883
TOPIC = "factory/+/telemetry"


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT broker!")
    print(f"Subscribing to: {TOPIC}")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    print(f"\nReceived message from: {msg.topic}")

    message = msg.payload.decode()

    process_telemetry(message)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

client.loop_forever()