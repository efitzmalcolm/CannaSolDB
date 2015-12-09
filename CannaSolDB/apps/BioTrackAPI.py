import os
import csv
import requests
from CannaSolDB.apps.retailers.models import Retailer


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
        raise ValueError('%(error)s' % response)


def syncVendors(transaction_start=Retailer.objects.latest('transactionid').values('transactionid')):
    action = 'sync_vendor'
    payload = {
        'API': API_VERSION,
        'action': action,
        'sessionid': login(),
        'transacton_start': transaction_start,
        }
    response = requests.post(URL, json=payload, headers=headers).json()

    if response['success']:
        return response
    else:
        raise ValueError('%(error)s' % response)
