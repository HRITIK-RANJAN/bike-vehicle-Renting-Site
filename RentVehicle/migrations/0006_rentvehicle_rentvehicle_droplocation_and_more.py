# Generated by Django 4.1.7 on 2023-04-10 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RentVehicle', '0005_rename_advance_amount_rentvehicle_amount_tobepaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentvehicle',
            name='RentVehicle_DropLocation',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='rentvehicle',
            name='RentVehicle_PickupLocation',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
