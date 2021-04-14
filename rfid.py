
from mfrc522 import SimpleMFRC522
from time import sleep
import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO
import threading
import led

def connect_mqtt():
    client = mqtt.Client(client_id)
    client.connect(broker, port)
    client.on_disconnect = on_disconnect
    return client


def publish(client, topic, message):
    result = client.publish(topic, message)
    print(result)

def on_disconnect(client, userdata, rc):
    print('DISCONNECTED! rc:', str(rc))

def on_message(client, userdata, message):
    print('message received!')
    payload = json.loads(message.payload)
    color = payload['value']
    led.turn_off_all()
    led.turn_on(color)

reader = SimpleMFRC522()
# client_id = 'tag-730707006997'
client_id = None
broker = '192.168.1.167'
port = 1883
topic_device = '/device/'
topic_device_control = '/device/control'
try:
    client = connect_mqtt()
    client.subscribe(topic_device_control)
    client.on_message = on_message
    thread = threading.Thread(target=client.loop_forever)
    thread.start()
    while True:
        led.turn_off_all()
        print("Hold a tag near the reader")
        id, text = reader.read()
        print(id, text)
        client_id = 'tag-' + str(id)
        message = {
            'sensor_id': client_id,
            'type_sensor': 'rfid',
            'type_value': 'fundsSource',
            'value': text.rstrip("\n")
        }
        publish(client, topic_device, json.dumps(message))
        sleep(5)
        
finally:
    print('error occured!!')
    GPIO.cleanup()


# try:
#         text = input('New data:')
#         print("Now place your tag to write")
#         reader.write(text)
#         print("Written")
# finally:
#         GPIO.cleanup()

