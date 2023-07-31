from django.db import models
from payments.models import Payments
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Manager(models.Model):
    Manager_id = models.AutoField
    Manager_firstname = models.CharField(max_length=60)
    Manager_lastname = models.CharField(max_length=60)
    Manager_address = models.CharField(max_length=600)
    Manager_email = models.CharField(max_length=100)
    Manager_password = models.CharField(max_length=32)
    Manager_dob = models.DateField()
    Manager_mobileno = models.CharField(max_length=10)
    Manager_gender = models.CharField(max_length=15)
    Manager_license = models.ImageField(upload_to='img/Manager_License/')
    Manager_agency = models.CharField(max_length=100,default="Fast Rentals")
    Manager_city = models.CharField(max_length=30)
    Manager_state = models.CharField(max_length=30)
    Manager_country = models.CharField(max_length=30)
    Manager_pincode = models.IntegerField()
    Manager_balance=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    isOwner = models.BooleanField(default=False)

    def __str__(self):
        return self.Manager_email + ": " + str(self.Manager_license)
    
@receiver(post_save, sender=Payments)
def update_manager_balance(sender, instance, **kwargs):
    reciever= instance.Payments_reciever
    manager = Manager.objects.filter(Manager_email=reciever)
    if manager:
        manager=Manager.objects.get(Manager_email=reciever)
        manager.Manager_balance +=instance.Payments_amount
        manager.save()
