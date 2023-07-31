from django.db import models
from Vehicles.models import Vehicle
from CustomerHome.models import Customer
from Owner.models import Owner
from Manager.models import Manager
from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.models import Payments

# Create your models here.
class RentVehicle(models.Model):
    RentVehicle_id = models.AutoField
    RentVehicle_Date_of_Booking = models.DateField(blank=True,null=True)
    RentVehicle_Date_of_Return = models.DateField(blank=True,null=True)
    RentVehicle_PickupLocation = models.CharField(blank=True,null=True, max_length=200)
    RentVehicle_DropLocation = models.CharField(blank=True,null=True, max_length=200)
    Total_days = models.IntegerField()
    Amount_Paid = models.IntegerField(blank=True,null=True)
    RentVehicle_Total_amount = models.IntegerField(blank=True,null=True)
    isAvailable = models.BooleanField(default=True)
    isBillPaid = models.BooleanField(default=False)
    Vehicle_license_plate = models.CharField(max_length=30)
    customer_email = models.CharField(max_length=100)
    request_responded_by = models.CharField(max_length=100,blank=True,null=True)
    request_status = models.CharField(max_length=30,default="Pending")

    def __str__(self):
        return self.customer_email + ": " + str(self.Vehicle_license_plate)+ "  |  STATUS :"+ self.request_status
    
@receiver(post_save, sender=Payments)
def update_rentvehicle(sender, instance, **kwargs):
    reciever= instance.Payments_reciever
    sender_r = instance.Payments_sender
    amount = instance.Payments_amount
    date = instance.Vehicle_BookingDate
    rentvehicle=RentVehicle.objects.filter(customer_email = sender_r , request_responded_by=reciever , RentVehicle_Total_amount = amount,isBillPaid=False,RentVehicle_Date_of_Booking=date)
    if rentvehicle:
        rentvehicle=RentVehicle.objects.get(customer_email = sender_r , request_responded_by=reciever , RentVehicle_Total_amount = amount,isBillPaid=False,RentVehicle_Date_of_Booking=date)
        rentvehicle.isBillPaid = True
        rentvehicle.Amount_Paid =amount
        rentvehicle.save()

# @receiver(post_save, sender=RentVehicle)
# def update_rentvehicle_pickup(sender, instance, **kwargs):
#     pass
        