import os
import csv
import requests


URL = 'https://wslcb.mjtraceability.com/serverjson.asp'
API_VERSION = '4.0'
USERNAME = os.environ.get('WSLCB_USER', '')
PASSWORD = os.environ.get('WSLCB_PASS', '')
UBI = '603324011'

headers = {'content-type': 'text/JSON'}

def login():
    action = 'login'
    payload = {
        'API': API_VERSION,
        'action': action,
        'username': USERNAME,
        'password': PASSWORD,
        'license_number': UBI,
        }
    response = requests.post(URL, json=payload, headers=headers).json()

    if response['success']:
        return response['sessionid']
    else:
        raise ValueError('Error: %s' % response['error'])
