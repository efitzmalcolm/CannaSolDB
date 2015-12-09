from django.db import models


class Retailer(models.Model):
    name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50,UnboundLocalError=True,blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip5 = models.CharField(max_length=5)
    zip4 = models.CharField(max_length=4)
    long = models.CharField(max_length=25)
    lat = models.CharField(max_length=25)
    ubi = models.CharField(max_length=9)
    location = models.CharField(max_length=25)
    locationtype = models.CharField(max_length=1)
    producer = models.BooleanField()
    processor = models.BooleanField()
    retail = models.BooleanField()
    transactionid = models.CharField(max_length=50)
    transactionid_original = models.CharField(max_length=50)

    class __str__(self):
        return self.name

