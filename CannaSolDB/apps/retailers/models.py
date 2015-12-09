from django.db import models


class Retailer(models.Model):
    name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50,null=True,blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip5 = models.CharField(max_length=5)
    zip4 = models.CharField(max_length=4,null=True,blank=True)
    long = models.CharField(max_length=25,null=True,blank=True)
    lat = models.CharField(max_length=25,null=True,blank=True)
    ubi = models.CharField(max_length=9)
    license_number = models.CharField(max_length=25)
    locationtype = models.CharField(max_length=1)
    producer = models.BooleanField()
    processor = models.BooleanField()
    retail = models.BooleanField()
    transactionid = models.CharField(max_length=50,unique=True)
    transactionid_original = models.CharField(max_length=50)

    class Meta:
        unique_together = ('license_number','ubi')

    def __str__(self):
        return self.name

