from os import terminal_size
import paho.mqtt.client as mqtt

terminal_id = "TO"
broker = "localhost"

client = mqtt.Client()

def call_worker(worker_name):
    client.publish("worker/name", worker_name + "." + terminal_id)

def connect_to_broker():
    client.connect(broker)
    call_worker("Client connected")

def disconnect_from_broker():
    call_worker("Client disconnected")
    client.disconnect()

def run_sender():
    connect_to_broker()
    while input() != "q":
        call_worker("INPUT DETECTED")
    disconnect_from_broker()

if __name__ == "__main__":
    run_sender()