
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
    print('Received!')
    topic = message.topic
    payload = message.payload
    if(topic == topic_rfid):
        publish(client, '/backend/', payload)
    elif(topic == topic_backend):
        payload = json.loads(payload)
        sensor_id = 'rgb-1'
        type_sensor = 'rgb-led'
        type_value = 'switch_led'
        value = None
        if (payload['type_message'] == 'payment_request'):
            if(payload['status'] == 'success'):
                value = 'blue'
            elif(payload['status'] == 'refused'):
                value = 'red'
        elif(payload['type_message'] == 'payment_process'):
            if(payload['status'] == 'success'):
                value = 'green'
            elif(payload['status'] == 'refused'):
                value = 'red'
        message = {
            'sensor_id': sensor_id,
            'type_sensor': type_sensor,
            'type_value': type_value,
            'value': value
        }
        publish(client, '/device/control', json.dumps(message))

def on_connect(client, userdata, flags, rc):
    print('Connected!')

client_id = 'service'
broker = '192.168.1.167'
port = 1883
topic_rfid = '/device/'
topic_backend = '/backend/control'

client = connect_mqtt()
client.on_connect = on_connect
client.on_message = on_message
client.subscribe(topic_rfid)
client.subscribe(topic_backend)
client.loop_forever()
