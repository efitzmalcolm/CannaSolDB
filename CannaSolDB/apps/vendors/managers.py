from django.db import models

class VendorManager(models.Manager):

    def get_queryset(self):
        return VendorQuerySet(self.model, using=self._db)

    def getByLicenseNum(self, license_num):
        return self.get_queryset().filter(license_number=license_num).latest('transactionid')

    def retailers(self):
        return self.get_queryset().retailers()


class VendorQuerySet(models.QuerySet):

    def retailers(self):
        return self.filter(retail=True)