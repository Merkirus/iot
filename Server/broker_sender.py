import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import datetime
import time
import adafruit_bme280.advanced as adafruit_bme280

buzzerPin = 23
terminal_id = "TO"
broker = "localhost"

prevResult = None
timer = None

GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.output(buzzerPin, 1)

client = mqtt.Client()

def call_worker(worker_name):
    client.publish("card/id", worker_name + "." + terminal_id)

def connect_to_broker():
    client.connect(broker)
    call_worker("Client connected")

def disconnect_from_broker():
    call_worker("Client disconnected")
    client.disconnect()

def rfidRead():
    MIFAREReader = MFRC522()

    num = 0
    uid = ""

    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        (status, uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            for i in range(0, len(uid)):
                num += uid[i] << (i*8)
            return str(uid), str(num)

    return None


def buzzer(state):
    GPIO.output(buzzerPin, not state)
    time.sleep(0.1)

def run_sender():
    connect_to_broker()
    while True:
        result = rfidRead()
        global prevResult
        global timer
        if (result):
            if (prevResult == result):
                buzzer(False)
                pass
            else:
                # uid = result[0]
                num = result[1]
                timer = datetime.datetime.now()
                call_worker(f"{num}")
                buzzer(True)

            prevResult = result
        else:
            if (prevResult and timer):
                buzzer(False)
                timer = None
                prevResult = None
    disconnect_from_broker()

if __name__ == "__main__":
    run_sender()
    GPIO.cleanup()