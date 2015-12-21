from django.db import models
from django.utils import timezone


class Inventory(models.Model):
    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField(editable=False)

    sessiontime = models.DateTimeField()
    transactionid = models.IntegerField()
    transactionid_original = models.IntegerField()
    deleted = models.BooleanField()

    currentroom = models.PositiveSmallIntegerField(blank=True, null=True)
    location = models.CharField(max_length=30)
    inventorystatus = models.PositiveSmallIntegerField(blank=True, null=True)
    inventorystatustime = models.DateTimeField(null=True)

    barcode = models.CharField(max_length=16)
    inventorytype = models.PositiveSmallIntegerField()
    productname = models.CharField(max_length=120,blank=True, null=True)
    strain = models.CharField(max_length=30,blank=True, null=True)

    remaining_qty = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    usable_weight = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    
    inventoryparentid = models.CharField(max_length=160,blank=True, null=True) # QA testing parent
    parentid = models.TextField(max_length=1600,blank=True, null=True) # Direct Parents
    plantid = models.TextField(max_length=1600,blank=True, null=True)
    mother_id = models.CharField(max_length=16,blank=True, null=True)

    seized = models.BooleanField(default=False)
    wet = models.BooleanField(default=False)
    is_sample = models.BooleanField(default=False)

    net_package = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()

        if self.seized is None:
            self.seized = False
        if self.wet is None:
            self.wet = False
        if self.is_sample is None:
            self.is_sample = False
        super(Inventory, self).save(*args, **kwargs)