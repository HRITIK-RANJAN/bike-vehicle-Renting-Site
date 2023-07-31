from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.models import Payments

# Create your models here.
class Owner(models.Model):
    Owner_id = models.AutoField
    Owner_firstname = models.CharField(max_length=60)
    Owner_lastname = models.CharField(max_length=60)
    Owner_address = models.CharField(max_length=600)
    Owner_email = models.CharField(max_length=100)
    Owner_password = models.CharField(max_length=32)
    Owner_dob = models.DateField()
    Owner_mobileno = models.CharField(max_length=10)
    Owner_gender = models.CharField(max_length=15)
    Owner_license =  models.ImageField(upload_to='img/Owner_License/')
    Owner_agency = models.CharField(max_length=100)
    Owner_city = models.CharField(max_length=30)
    Owner_state = models.CharField(max_length=30)
    Owner_country = models.CharField(max_length=30)
    Owner_pincode = models.IntegerField()
    Owner_balance=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    isOwner = models.BooleanField(default=True)

    def __str__(self):
        return "Name : "+self.Owner_firstname + " " +self.Owner_lastname + "  |   Email : "+ self.Owner_email
    
@receiver(post_save, sender=Payments)
def update_owner_balance(sender, instance, **kwargs):
    reciever= instance.Payments_reciever
    owner = Owner.objects.filter(Owner_email=reciever)
    if owner:
        owner=Owner.objects.get(Owner_email=reciever)
        owner.Owner_balance +=instance.Payments_amount
        owner.save()