import os
import csv
import datetime
import decimal
import requests
from django.db import IntegrityError, transaction
from django.db.models import Sum
from django.utils import timezone
from CannaSolDB.apps.vendors.models import Vendor
from CannaSolDB.apps.transfers.models import Transfer, Manifest, ManifestStop, ManifestItem
from CannaSolDB.apps.inventory.models import Inventory


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

def syncCheck(table,sum,download=True):
    action = 'sync_check'
    payload = {
        'API': API_VERSION,
        'action': action,
        'sessionid': login(),
        'download': download,
        'data': {
            'table': table,
            'sum': sum,
            'active': 0,
            }
        }
    response = requests.post(URL, json=payload, headers=headers).json()

    if response['success']:
        return response
    else:
        raise ValueError('%(error)s' % response)

def syncAll():
    syncVendors()
    syncInventory()
    syncManifests()
    syncTransfers()


@transaction.atomic
def syncVendors():
    print('Sync Vendors:')
    table = 'vendor'
    sum = Vendor.objects.aggregate(Sum('transactionid'))['transactionid__sum']

    response = syncCheck(table,sum)

    if response['summary'][0]['match'] == False:
        print('Out of Sync.Syncing Vendors...')
        print('')
        total = 0
        new = 0
        renamed = 0
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
            

            # Handle Name Changes
            try:
                v = Vendor.objects.get(ubi=args['ubi'], license_number=args['license_number'])
                if v.name != args['name']:
                    v.prev_name = v.name
                    v.name = args['name']
                    v.save()
                    renamed = renamed + 1
            except Vendor.DoesNotExist:
                v = Vendor(**args)
                v.save()
                v.getCoords()
                new = new + 1
            total = total + 1

        print('Total Records: %s' % total)
        print('New Records: %s' % new)
        print('Names Changes: %s' % new)

    else:
        print('Already current with State')


@transaction.atomic
def syncTransfers():
    print('Sync Transfers:')
    table = 'inventory_transfer'
    sum = Transfer.objects.aggregate(Sum('transactionid'))['transactionid__sum']

    response = syncCheck(table,sum)

    if response['summary'][0]['match'] == False:
        print('Out of Sync. Syncing Transfers...')
        print('')
        total = 0
        new = 0
        for x in response['inventory_transfer']:
            args = {
                'deleted': x['deleted'],
                'inventorytype': x['inventorytype'],
                'location': x['location'],
                'manifest_stop': x['manifest_stop'],
                'manifestid': x['manifestid'],
                'outbound_license': x['outbound_license'],
                'lineprice': x['price'],
                'qty': x['quantity'],
                'strain': x['strain'],
                'transactionid': x['transactionid'],
                'transactionid_original': x['transactionid_original'],
                'sessiontime': datetime.datetime.fromtimestamp(
                    int(x['sessiontime']), timezone.get_current_timezone()),
                'inventoryid': x['inventoryid']
                }

            try:
                t = Transfer.objects.get(**args)
            except Transfer.DoesNotExist:
                t = Transfer(**args)
                t.save()
                new = new + 1
            total = total + 1

        print('Total Records: %s' % total)
        print('New Records: %s' % new)

    else:
        print('Already current with State')


@transaction.atomic
def syncManifests():
    print('Sync Manifests:')
    table = 'manifest'
    sum = Manifest.objects.aggregate(Sum('transactionid'))['transactionid__sum']

    response = syncCheck(table,sum)

    if response['summary'][0]['match'] == False:
        print('Out of Sync. Syncing Manifests...')
        print('')
        total = 0
        new = 0
        for x in response['manifest']:
            args = {
                'deleted': x['deleted'],
                'from_location': x['location'],
                'stopcount': x['stopcount'],
                'manifestid': x['manifestid'],
                'transactionid': x['transactionid'],
                'transactionid_original': x['transactionid_original'],
                'sessiontime': datetime.datetime.fromtimestamp(
                    int(x['sessiontime']), timezone.get_current_timezone()),
                'total_item_count': x['total_item_count'],
                'transporter_dob': x['transporter_dob'],
                'transporter_id': x['transporter_id'],
                'transporter_name': x['transporter_name'],
                'transporter_vehicle_details': x['transporter_vehicle_details'],
                'transporter_vehicle_identification': x['transporter_vehicle_identification'],
                }

            try:
                t = Manifest.objects.get(**args)
            except Manifest.DoesNotExist:
                t = Manifest(**args)
                t.save()
                new = new + 1
            total = total + 1
        print('Total Records: %s' % total)
        print('New Records: %s' % new)

        total = 0
        new = 0
        print('Syncing Manifest Stops...')
        for x in response['manifest_stop_data']:
            args = {
                'deleted': x['deleted'],
                'stopnumber': x['stopnumber'],
                'manifestid': x['manifestid'],
                'transactionid': x['transactionid'],
                'transactionid_original': x['transactionid_original'],
                'sessiontime': datetime.datetime.fromtimestamp(
                    int(x['sessiontime']), timezone.get_current_timezone()),
                'item_count': x['item_count'],
                'arrive_time': datetime.datetime.fromtimestamp(
                    int(x['arrive_time']), timezone.get_current_timezone()),
                'city': x['city'],
                'depart_time': datetime.datetime.fromtimestamp(
                    int(x['depart_time']), timezone.get_current_timezone()),
                'license_number': x['license_number'],
                'name': x['name'],
                }

            try:
                t = ManifestStop.objects.get(**args)
            except ManifestStop.DoesNotExist:
                t = ManifestStop(**args)
                t.save()
                new = new + 1
            total = total + 1
        print('Total Records: %s' % total)
        print('New Records: %s' % new)

        total = 0
        new = 0
        noitem = 0
        print('Syncing Manifest Items...')
        for x in response['manifest_stop_items']:
            args = {
                'deleted': x['deleted'],
                'stopnumber': x['stopnumber'],
                'manifestid': x['manifestid'],
                'transactionid': x['transactionid'],
                'transactionid_original': x['transactionid_original'],
                'sessiontime': datetime.datetime.fromtimestamp(
                    int(x['sessiontime']), timezone.get_current_timezone()),
                'description': x['description'],
                'qty':  decimal.Decimal(x['quantity']),
                'inventoryid': x['inventoryid'],
                }

            try:
                t = ManifestItem.objects.get(**args)
            except ManifestItem.DoesNotExist:
                t = ManifestItem(**args)
                t.save()
                new = new + 1
            total = total + 1
        print('Total Records: %s' % total)
        print('New Records: %s' % new)

    else:
        print('Already current with State')


@transaction.atomic
def syncInventory():
    print('Sync Inventory:')
    table = 'inventory'
    sum = Inventory.objects.aggregate(Sum('transactionid'))['transactionid__sum']

    response = syncCheck(table,sum)

    if response['summary'][0]['match'] == False:
        print('Out of Sync. Syncing Inventory...')
        print('')
        total = 0
        new = 0
        for x in response['inventory']:
            args = {
                'sessiontime': datetime.datetime.fromtimestamp(
                    int(x['sessiontime']), timezone.get_current_timezone()),
                'transactionid': x['transactionid'],
                'transactionid_original': x['transactionid_original'],
                'deleted': x['deleted'],

                'currentroom': x['currentroom'],
                'location': x['location'],
                'inventorystatus': x['inventorystatus'],
                'barcode': x['id'],
                'inventorytype': x['inventorytype'],
                'productname': x['productname'],
                'strain': x['strain'],

                'remaining_qty': x['remaining_quantity'],
                'usable_weight': x['usable_weight'],
    
                'inventoryparentid': x['inventoryparentid'],
                'parentid': x['parentid'],
                'plantid': x['plantid'],
                'mother_id': x['source_id'],

                'seized': x['seized'],
                'wet': x['wet'],
                'is_sample': x['is_sample'],

                'net_package': x['net_package']
                }
            
            try:
                args['inventorystatustime'] = datetime.datetime.fromtimestamp(
                    int(x['inventorystatustime']), timezone.get_current_timezone())
            except TypeError:
                args['inventorystatustime'] = None


            try:
                t = Inventory.objects.get(barcode=x['id'])
            except Inventory.DoesNotExist:
                t = Inventory(**args)
                t.save()
                new = new + 1
            total = total + 1

        print('Total Records: %s' % total)
        print('New Records: %s' % new)

        

    else:
        print('Already current with State')