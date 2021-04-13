
from mfrc522 import SimpleMFRC522
from time import sleep
import paho.mqtt.client as mqtt
import json

def connect_mqtt():
    client = mqtt.Client(client_id)
    client.connect(broker, port)
    return client


def publish(client, topic, message):
    result = client.publish(topic, message)
    print(result)

reader = SimpleMFRC522()
client_id = 'tag-730707006997'
broker = '192.168.1.167'
port = 1883
topic = '/rfid/read'

try:
    client = connect_mqtt()
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        text = 'wallet'
        message = {
            'sensorId': client_id,
            'typeSensor': 'rfid',
            'typeValue': 'fundsSource',
            'value': text
        }
        publish(client, topic, json.dumps(message))
        sleep(5)
finally:
    print('error occured!!')


# try:
#         text = input('New data:')
#         print("Now place your tag to write")
#         reader.write(text)
#         print("Written")
# finally:
#         GPIO.cleanup()

