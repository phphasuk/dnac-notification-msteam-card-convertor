#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Phithakkit Phasuk"
__email__ = "phphasuk@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


import urllib3
import json
import os
import time
import datetime
import requests
from jinja2 import Environment, FileSystemLoader

from flask import Flask, request
from flask_basicauth import BasicAuth

from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings


os.environ['TZ'] = 'America/Los_Angeles'  # define the timezone for PST
time.tzset()  # adjust the timezone, more info https://help.pythonanywhere.com/pages/SettingTheTimezone/

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

from config import WEBHOOK_HOST, WEBHOOK_PORT, WEBHOOK_USERNAME, WEBHOOK_PASSWORD, TEAM_WEBHOOK_URL


app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = WEBHOOK_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = WEBHOOK_PASSWORD
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)


@app.route('/')  # create a page for testing the flask framework
@basic_auth.required
def index():
    return '<h1>Flask Receiver App is Up!</h1>', 200


@app.route('/webhook', methods=['POST'])  # create a route for /webhook, method POST
@basic_auth.required
def webhook():
    if request.method == 'POST':
        print('Webhook Received')
        request_json = request.json

        # print the received notification
        print('Payload: ')
        print(json.dumps(request_json, indent=4))

        # save as a file, create new file if not existing, append to existing file
        # full details of each notification to file 'in_webhook_payload.json'

        with open('in_webhook_payload.json', 'a') as file:
            file.write('%s\n' % json.dumps(request_json, indent=4))

        card = make_adaptive_card(request_json)
        post_request(card)

        return 'Webhook notification received', 200
    else:
        return 'Method not supported', 405


def make_adaptive_card(data):
    details_data = []
    for item in data['details']:
        details_data.append(f'- {item}: {data["details"][item]}')
    if not data.get('dnacIP'):
        data['dnacIP'] = 'Not Provided'
    j2_env = Environment(loader=FileSystemLoader('.'))
    adaptive_Card_template = j2_env.get_template('adaptive_card_template.j2')
    adaptive_card = adaptive_Card_template.render(
        instanceId = data['instanceId'],
        eventId = data['eventId'],
        name = data['name'],
        description = data['description'],
        timestamp = datetime.datetime.fromtimestamp(data['timestamp']/1000.0).strftime('%Y-%m-%d %H:%M:%S.%f'),
        dnacIP = data['dnacIP'],
        details = '\\r'.join(details_data),
        ciscoDnaEventLink = data['ciscoDnaEventLink']
    )
    return adaptive_card


def post_request(data):
    url = TEAM_WEBHOOK_URL
    payload = data
    headers = {
            'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url=url, headers=headers, data=payload, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err) 


if __name__ == '__main__':
#    with open('sample_data.json', 'r') as file:
#        read_data = json.load(file)
#    card = make_adaptive_card(read_data)
#    post_request(card)
    app.run(host=WEBHOOK_HOST, port=WEBHOOK_PORT, ssl_context='adhoc', debug=True)

