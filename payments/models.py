from django.db import models

# Create your models here.
class Payments(models.Model):
    Payments_id=models.AutoField
    Payments_sender=models.CharField(max_length=100,blank=True,null=True)
    Payments_reciever=models.CharField(max_length=100,blank=True,null=True)
    Payments_date=models.DateTimeField(blank=True,null=True)
    Payments_amount=models.DecimalField(max_digits=10, decimal_places=2)
    Vehicle_BookingDate = models.DateField(blank=True,null=True)

    def __str__(self) :
        return  "Sender : " + self.Payments_sender + " |   Amount: "+ str(self.Payments_amount)