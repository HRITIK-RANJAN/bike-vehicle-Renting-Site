from django.shortcuts import render , redirect
from CustomerHome.models import Customer
from Owner.models import Owner
from Manager.models import Manager
from Vehicles.models import Vehicle
from RentVehicle.models import RentVehicle
from.models import Payments
from datetime import datetime



# Create your views here.
def index(request):
    return render(request,'payments/index.html')

def completePayment(request,RentVehicle_Date_of_Booking):
    sender_email = request.session.get('user_email')
    rentvehicle = RentVehicle.objects.get(customer_email=sender_email,RentVehicle_Date_of_Booking=RentVehicle_Date_of_Booking)
    Vehicle_BookingDate=rentvehicle.RentVehicle_Date_of_Booking
    receiver_email=rentvehicle.request_responded_by
    amount=rentvehicle.RentVehicle_Total_amount
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    date = dt_string
    payment=Payments(Payments_sender=sender_email,
    Payments_reciever=receiver_email,
    Payments_date=date,
    Payments_amount=amount,
    Vehicle_BookingDate=Vehicle_BookingDate)
    payment.save()

    # print("----------------------------", amount)
    context={'sender_email':sender_email,'receiver_email':receiver_email,'amount':amount,'date':date}
    return render(request,'payments/completePayment.html',context)


