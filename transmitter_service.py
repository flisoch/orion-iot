
from time import sleep
import threading
import paho.mqtt.client as mqtt
import json

def connect_mqtt():
    client = mqtt.Client(client_id)
    client.connect(broker, port)
    return client


def publish(client, topic, message):
    result = client.publish(topic, message)
    print('Published!')

def on_message(client, userdata, message):
    topic = message.topic
    payload = json.loads(message.payload)
    print('Received!')
    publish(client, '/backend' + topic, message.payload)

def on_connect(client, userdata, flags, rc):
    print('Connected!')

client_id = 'service'
broker = '192.168.1.167'
port = 1883
topic = '/rfid/read'


client = connect_mqtt()
client.on_connect = on_connect
client.on_message = on_message
client.subscribe(topic)
client.loop_forever()
