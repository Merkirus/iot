import paho.mqtt.client as mqtt
from request_handler import RequestHandler

broker = "10.108.33.125"

client = mqtt.Client()

current_message = ""

def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")

    current_message = message_decoded[0]

    print(f'message: {message_decoded}')

    if current_message.isdigit():
        req = RequestHandler("http://localhost:8000")
        req.post_card(current_message)
    


def connect_to_broker():
    client.connect(broker)
    client.on_message = process_message
    client.loop_start()
    client.subscribe("card/id")

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