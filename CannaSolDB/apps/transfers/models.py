from django.db import models
from django.utils import timezone


class Transfer(models.Model):
    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField(editable=False)

    sessiontime = models.DateTimeField()
    transactionid = models.IntegerField()
    transactionid_original = models.IntegerField()
    deleted = models.BooleanField()

    inventoryid = models.CharField(max_length=16)
    inventorytype = models.CharField(max_length=2) # Convert to FK
    strain = models.CharField(max_length=50)

    lineprice = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.DecimalField(max_digits=10, decimal_places=2)

    manifestid = models.CharField(max_length=16) # COnvert to FK
    manifest_stop = models.PositiveSmallIntegerField()
    location = models.CharField(max_length=50)
    outbound_license = models.CharField(max_length=50)


    def __str__(self):
        return '%s: %s - %s units @ $%s' % (self.sessiontime, self.inventoryid, self.qty, self.lineprice)

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        super(Transfer, self).save(*args, **kwargs)

class Manifest(models.Model):
    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField(editable=False)

    sessiontime = models.DateTimeField()
    transactionid = models.IntegerField()
    transactionid_original = models.IntegerField()
    deleted = models.BooleanField()

    manifestid = models.CharField(max_length=16)
    stopcount = models.PositiveSmallIntegerField()

    from_location = models.CharField(max_length=50)

    total_item_count = models.PositiveSmallIntegerField()

    transporter_dob = models.CharField(max_length=50)
    transporter_id = models.CharField(max_length=50)
    transporter_name = models.CharField(max_length=50)
    transporter_vehicle_details = models.CharField(max_length=50)
    transporter_vehicle_identification = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        super(Manifest, self).save(*args, **kwargs)


class ManifestStop(models.Model):
    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField(editable=False)

    sessiontime = models.DateTimeField()
    transactionid = models.IntegerField()
    transactionid_original = models.IntegerField()
    deleted = models.BooleanField()

    manifestid = models.CharField(max_length=16)
    stopnumber = models.PositiveSmallIntegerField()

    arrive_time = models.DateTimeField()
    depart_time = models.DateTimeField()

    item_count = models.PositiveSmallIntegerField()
    license_number = models.CharField(max_length=50)
    
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    class Meta:
        unique_together = ('manifestid','stopnumber')

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        super(ManifestStop, self).save(*args, **kwargs)


class ManifestItem(models.Model):
    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField(editable=False)

    sessiontime = models.DateTimeField()
    transactionid = models.IntegerField()
    transactionid_original = models.IntegerField()
    deleted = models.BooleanField()

    manifestid = models.CharField(max_length=16)
    stopnumber = models.PositiveSmallIntegerField()

    inventoryid = models.CharField(max_length=16)
    description = models.CharField(max_length=100)
    qty = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        super(ManifestItem, self).save(*args, **kwargs)

