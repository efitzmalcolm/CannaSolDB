from django.db import models
from django.utils import timezone
from CannaSolDB.apps.vendors.managers import VendorManager
from geopy.geocoders import GoogleV3


class Vendor(models.Model):
    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField(editable=False)

    name = models.CharField(max_length=100)
    prev_name = models.CharField(max_length=100,null=True,blank=True)

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

    transactionid = models.IntegerField()
    transactionid_original = models.IntegerField()

    objects = VendorManager()

    class Meta:
        unique_together = ('license_number', 'ubi')


    def __str__(self):
        return self.name


    def getCoords(self):
        if self.retail:
            if not self.long or not self.lat:
                geolocator = GoogleV3()
                loc = geolocator.geocode('%s %s %s' % (self.address1, self.city, self.state),timeout=1.5)
                self.long = loc.longitude
                self.lat = loc.latitude
                self.save()
            return (self.lat, self.long)

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        super(Vendor, self).save(*args, **kwargs)
