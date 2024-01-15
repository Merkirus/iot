import paho.mqtt.client as mqtt
from .requests import Request

broker = "10.108.33.129"

client = mqtt.Client()

current_message = ""

def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")

    current_message = message_decoded[0]

    timestamp = ""
    uuid = ""

    req = Request("127.0.0.1:8000")
    req.post_json((timestamp, uuid))
    
    print(current_message)

def connect_to_broker():
    client.connect(broker)
    client.on_message = process_message
    client.loop_start()
    client.subscribe("worker/name")

def disconnect_from_broker():
    client.loop_stop()
    client.disconnect()

def run_receiver():
    connect_to_broker()
    while current_message != "Client disconnected":
        pass
    disconnect_from_broker()

if __name__ == "__main__":
    run_receiver()