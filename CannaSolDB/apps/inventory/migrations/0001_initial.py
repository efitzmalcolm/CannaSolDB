# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 04:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(editable=False)),
                ('modified_date', models.DateTimeField(editable=False)),
                ('sessiontime', models.DateTimeField()),
                ('transactionid', models.IntegerField()),
                ('transactionid_original', models.IntegerField()),
                ('deleted', models.BooleanField()),
                ('currentroom', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('location', models.CharField(max_length=30)),
                ('inventorystatus', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('inventorystatustime', models.DateTimeField(null=True)),
                ('barcode', models.CharField(max_length=16)),
                ('inventorytype', models.PositiveSmallIntegerField()),
                ('productname', models.CharField(blank=True, max_length=120, null=True)),
                ('strain', models.CharField(blank=True, max_length=30, null=True)),
                ('remaining_qty', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('usable_weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('inventoryparentid', models.CharField(blank=True, max_length=160, null=True)),
                ('parentid', models.TextField(blank=True, max_length=1600, null=True)),
                ('plantid', models.TextField(blank=True, max_length=1600, null=True)),
                ('mother_id', models.CharField(blank=True, max_length=16, null=True)),
                ('seized', models.BooleanField(default=False)),
                ('wet', models.BooleanField(default=False)),
                ('is_sample', models.BooleanField(default=False)),
                ('net_package', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
    ]