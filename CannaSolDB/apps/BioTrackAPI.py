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


def syncVendors():
    action = 'sync_vendor'
    try:
        last_transactionid = Retailer.objects.latest('transactionid').values('transactionid')
    except:
        last_transactionid = 0
    payload = {
        'API': API_VERSION,
        'action': action,
        'sessionid': login(),
        'transaction_start': last_transactionid + 1,
    }
    response = requests.post(URL, json=payload, headers=headers).json()

    if response['success']:
        for x in response['vendor']:
            args = {
                'name' : x['name'],
                'address1' : x['address1'],
                'address2' : x['address2'],
                'city' : x['city'],
                'state' : x['state'],
                'zip5' : x['zip'][:5],
                'ubi' : x['ubi'],
                'license_number' :x['location'],
                'locationtype' : x['locationtype'],
                'producer' : x['producer'],
                'processor' : x['processor'],
                'retail' : x['retail'],
                'transactionid' : x['transactionid'],
                'transactionid_original' : x['transactionid_original'],
            }
            if len(x['zip']) > 5:
                args['zip4'] = x['zip'][5:]
            
            Retailer.objects.create(**args)
                
    else:
        raise ValueError('%(error)s' % response)
