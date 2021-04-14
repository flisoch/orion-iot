from os import environ as env
from dotenv import load_dotenv, find_dotenv
import threading

from flask import Flask, request
import json
import requests

import paho.mqtt.client as mqtt

app = Flask(__name__)

client_id = env.get('CLIENT_ID')
client_oauth_code = env.get('CLIENT_OAUTH_CODE')
oauth_redirect_uri = env.get('OAUTH_REDIRECT_URI')


@app.route("/oauth")
def oauth():
    client_oauth_code = request.args.get('code')
    params = {
        'code': client_oauth_code,
        'client_id': client_id,
        'grant_type': 'authorization_code',
        'redirect_uri': oauth_redirect_uri
    }
    r = requests.post('https://yoomoney.ru/oauth/token', params=params)
    access_token = json.loads(r.text)['access_token']
    env['ACCESS_TOKEN'] = access_token
    return r.text


@app.route("/")
def hello():
    return """
    <html>
        <body>
            <div>
                <a href='/ym/account-info'> account-info</a>
            </div>
            <div>
                <a href='/ym/pay-phone-request'> payment-request</a>
            </div>
            <div>
                <a href='/ym/pay-phone-process'> payment-process</a>
            </div>
            <div>
                <a href='/ym/pay-phone-request-process'> payment-request-process</a>
            </div>
            <div>
                <a href='/ym/authorize'>authorize this client</a>
            </div>
        </body>
    </html>"""

@app.route("/ym/account-info")
def account_info():
    access_token = env.get('ACCESS_TOKEN')
    auth_header = "Bearer " + access_token
    headers = {"Authorization": auth_header}
    r = requests.post('https://yoomoney.ru/api/account-info', headers=headers)
    return r.text

@app.route("/ym/pay-phone-request-process")
def pay_phone_request_process():
    access_token = env.get('ACCESS_TOKEN')
    auth_header = "Bearer " + access_token
    headers = {"Authorization": auth_header}
    # request payment
    data = {
    'pattern_id': 'phone-topup', 
    'phone-number': env.get('PHONE_NUMBER'), 
    'amount': 10.00
    }
    r = requests.post('https://yoomoney.ru/api/request-payment', data=data, headers=headers)
    request_id = json.loads(r.text)['request_id']

    # process payment
    data1 = {
        'request_id':request_id
    }
    r1 = requests.post('https://yoomoney.ru/api/process-payment', data=data1, headers=headers)
    return r.text + '\n' + r1.text

@app.route("/ym/pay-phone-request")
def pay_phone_request():
    access_token = env.get('ACCESS_TOKEN')
    auth_header = "Bearer " + access_token
    headers = {"Authorization": auth_header}
    data = {
    'pattern_id': 'phone-topup', 
    'phone-number': env.get('PHONE_NUMBER'), 
    'amount': 10.00
    }
    r = requests.post('https://yoomoney.ru/api/request-payment', data=data, headers=headers)
    request_id = json.loads(r.text)['request_id']
    env['REQUEST_ID'] = request_id
    return r.text

@app.route("/ym/pay-phone-process")
def pay_phone_process(money_source='wallet'):
    access_token = env.get('ACCESS_TOKEN')
    auth_header = "Bearer " + access_token
    headers = {"Authorization": auth_header}
    if ('wallet' in money_source):
        data = {
        'request_id': env.get('REQUEST_ID')
        }
    else:
        data= {
        'request_id': env.get('REQUEST_ID'),
        'money_source':money_source,
        'csc':'999'
        }
    print(data)
    r = requests.post('https://yoomoney.ru/api/process-payment', data=data, headers=headers)
    print(r.status_code)
    print(r.text)
    return r.text



@app.route("/ym/authorize")
def authorize():
    params = {
    'client_id': client_id, 
    'response_type': 'code', 
    'redirect_uri': oauth_redirect_uri,
    'scope': 'account-info operation-history operation-details payment-p2p payment-shop money-source(\"wallet\",\"card\")'
    }
    r = requests.post('https://yoomoney.ru/oauth/authorize', params=params)
    print(r.status_code)
    return r.text

def mqtt_run():
    def on_message(client, userdata, message):
        print('Received!')
        topic = message.topic
        payload = json.loads(message.payload)
        fund_source = payload['value']
        print(fund_source)
        
        response = json.loads(pay_phone_request())
        status = response['status']
        if (status == 'success'):
            message = {
                'type_message':'payment_request',
                'status': 'success',
            }
        else:
            message = {
                'type_message':'payment_request',
                'status': 'refused',
                'error': response['error'],
                'error_description': response['error_description']
            }    
        result = client.publish('/backend/control', json.dumps(message))
        response = json.loads(pay_phone_process(fund_source))
        status = response['status']
        if (status == 'success'):
            message = {
                'type_message':'payment_process',
                'status':'success',
            }
        else:
            message = {
                'type_message':'payment_process',
                'status': 'refused',
                'error': response['error']
            } 
        result = client.publish('/backend/control', json.dumps(message))

    client = mqtt.Client('backend')
    broker = '192.168.1.167'
    port = 1883
    client.connect(broker, port)
    client.subscribe('/backend/')
    client.on_message = on_message
    return client


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    client = mqtt_run()
    thread = threading.Thread(target=client.loop_forever)
    thread.start()
    app.run(host=env.get('HOST_IP'), ssl_context='adhoc')