from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from Owner.models import Owner
from Manager.models import Manager
from CustomerHome.models import Customer
from Vehicles.models import Vehicle
from RentVehicle.models import RentVehicle

from datetime import datetime
from datetime import date

# Create your views here.
def index(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)
    vehicle = Vehicle.objects.all()
    Message="Welcome Aboard!!"
    no_of_pending_request=count_pending_rent_request()
    return render(request,'Manager_index.html',{'vehicle':vehicle,'Message':Message,'manager':manager,'no_of_pending_request':no_of_pending_request})

def Profile(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)
    no_of_pending_request=count_pending_rent_request()
    return render(request,'Manager_Profile.html',{'manager':manager,'no_of_pending_request':no_of_pending_request})

def AllCustomers(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)
    customer = Customer.objects.all()
    no_of_pending_request=count_pending_rent_request()
    return render(request,"Manager_All_Customers.html",{'customer':customer,'manager':manager,'no_of_pending_request':no_of_pending_request})

def Customer_Profile(request,customer_email):
    if('user_email' not in request.session):
        return redirect('/signin/')
    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)
    customer = Customer.objects.get(customer_email=customer_email)
    no_of_pending_request=count_pending_rent_request()
    return render(request,'Manager_Customer_Profile.html',{'manager':manager,'customer':customer,'no_of_pending_request':no_of_pending_request})

def upload_Vehicle(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)
    no_of_pending_request=count_pending_rent_request()
    return render(request,"Manager_Upload_Vehicle.html",{'manager':manager,'no_of_pending_request':no_of_pending_request})

def AllVehicles(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)
    vehicle = Vehicle.objects.all()
    no_of_pending_request=count_pending_rent_request()
    return render(request,"Manager_all_vehicles.html",{'vehicle':vehicle,'manager':manager,'no_of_pending_request':no_of_pending_request})

def showdetails(request,Vehicle_license_plate):
    if('user_email' not in request.session):
        return redirect('/signin/')
    vehicle = Vehicle.objects.get(Vehicle_license_plate=Vehicle_license_plate)
    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)
    no_of_pending_request=count_pending_rent_request()
    return render(request,'Manager_showdetails.html',{'vehicle':vehicle,'manager':manager,'no_of_pending_request':no_of_pending_request})

def CheckAvailability(request,Vehicle_license_plate):
    if('user_email' not in request.session):
        return redirect('/signin/')

    RentVehicle_Date_of_Booking=request.POST.get('RentVehicle_Date_of_Booking','')
    RentVehicle_Date_of_Return=request.POST.get('RentVehicle_Date_of_Return','')
    RentVehicle_DropLocation=request.POST.get('Drop_Locations','')

    RentVehicle_Date_of_Booking = datetime.strptime(RentVehicle_Date_of_Booking, '%Y-%m-%d').date()
    RentVehicle_Date_of_Return = datetime.strptime(RentVehicle_Date_of_Return, '%Y-%m-%d').date()

    rentvehicle = RentVehicle.objects.filter(Vehicle_license_plate=Vehicle_license_plate)
    vehicle = Vehicle.objects.get(Vehicle_license_plate=Vehicle_license_plate)

    customer_email = request.session.get('user_email')
    customer = Customer.objects.get(customer_email=customer_email)

# Changed ------------------------------------------------------------------
    vehiclePickup = RentVehicle.objects.filter(Vehicle_license_plate=Vehicle_license_plate, RentVehicle_Date_of_Booking__lt = RentVehicle_Date_of_Booking)
    n=vehiclePickup.count()
    if vehiclePickup and n>0:
        vehiclePickup= RentVehicle.objects.filter(Vehicle_license_plate=Vehicle_license_plate, RentVehicle_Date_of_Booking__lt = RentVehicle_Date_of_Booking,request_status="Accepted").last()
        #  or request not should be declined
        print("Status : "+str(vehiclePickup.request_status)+" Drop Location : "+str(vehiclePickup. RentVehicle_DropLocation)+ " Booking Date : "+str(vehiclePickup.RentVehicle_Date_of_Booking))
        vehiclePickupLocation=vehiclePickup.RentVehicle_DropLocation
    else:
        vehicle = Vehicle.objects.get(Vehicle_license_plate=Vehicle_license_plate)
        vehiclePickupLocation = vehicle.Vehicle_initial_location
# ----------------------------

    if RentVehicle_Date_of_Booking < date.today():
        Incorrect_dates = "Please give proper dates"
        return render(request,'showdetails_loggedin.html',{'Incorrect_dates':Incorrect_dates,'vehicle':vehicle,'customer':customer})

    if RentVehicle_Date_of_Return < RentVehicle_Date_of_Booking:
        Incorrect_dates = "Please give proper dates"
        return render(request,'showdetails_loggedin.html',{'Incorrect_dates':Incorrect_dates,'vehicle':vehicle,'customer':customer})
    
    days=(RentVehicle_Date_of_Return-RentVehicle_Date_of_Booking).days+1
    total=days*vehicle.Vehicle_price
    
    rent_data = {"RentVehicle_Date_of_Booking":RentVehicle_Date_of_Booking, "RentVehicle_Date_of_Return":RentVehicle_Date_of_Return,"days":days, "total":total}
    
    for rv in rentvehicle:

        if (rv.RentVehicle_Date_of_Booking >= RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return >= rv.RentVehicle_Date_of_Booking) or (RentVehicle_Date_of_Booking >= rv.RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return <= rv.RentVehicle_Date_of_Return) or (RentVehicle_Date_of_Booking <= rv.RentVehicle_Date_of_Return and RentVehicle_Date_of_Return >= rv.RentVehicle_Date_of_Return):
            if rv.isAvailable and rv.request_status=="Pending":
                Available = True
                Message = "Note that somebody has also requested for this vehicle from " + str(rv.RentVehicle_Date_of_Booking) + " to " + str(rv.RentVehicle_Date_of_Return)
                return render(request,'showdetails_loggedin.html',{'Message':Message,'Available':Available,'vehicle':vehicle,'customer':customer,'rent_data':rent_data})
            elif rv.request_status=="Accepted":
                NotAvailable = True
                return render(request,'showdetails_loggedin.html',{'NotAvailable':NotAvailable,'dates':rv,'vehicle':vehicle,'customer':customer})

        # if (RentVehicle_Date_of_Booking < rv.RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return < rv.RentVehicle_Date_of_Booking) or (RentVehicle_Date_of_Booking > rv.RentVehicle_Date_of_Return and RentVehicle_Date_of_Return > rv.RentVehicle_Date_of_Return):
        #     Available = True
        #     return render(request,'showdetails_loggedin.html',{'Available':Available,'vehicle':vehicle,'customer':customer,'rent_data':rent_data})


    Available = True
    return render(request,'showdetails_loggedin.html',{'Available':Available,'vehicle':vehicle,'customer':customer,'rent_data':rent_data,'vehiclePickupLocation':vehiclePickupLocation, 'RentVehicle_DropLocation':RentVehicle_DropLocation})

    if('user_email' not in request.session):
        return redirect('/signin/')

    RentVehicle_Date_of_Booking=request.POST.get('RentVehicle_Date_of_Booking','')
    RentVehicle_Date_of_Return=request.POST.get('RentVehicle_Date_of_Return','')
    RentVehicle_DropLocation=request.POST.get('Drop_Locations','')


    RentVehicle_Date_of_Booking = datetime.strptime(RentVehicle_Date_of_Booking, '%Y-%m-%d').date()
    RentVehicle_Date_of_Return = datetime.strptime(RentVehicle_Date_of_Return, '%Y-%m-%d').date()

    rentvehicle = RentVehicle.objects.filter(Vehicle_license_plate=Vehicle_license_plate)
    vehicle = Vehicle.objects.get(Vehicle_license_plate=Vehicle_license_plate)

    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)
    
# Changed ------------------------------------------------------------------
    vehiclePickup = RentVehicle.objects.filter(Vehicle_license_plate=Vehicle_license_plate, RentVehicle_Date_of_Booking__lt = RentVehicle_Date_of_Booking)
    n=vehiclePickup.count()
    if vehiclePickup and n>0:
        vehiclePickup= RentVehicle.objects.filter(Vehicle_license_plate=Vehicle_license_plate, RentVehicle_Date_of_Booking__lt = RentVehicle_Date_of_Booking,request_status="Accepted").last()
        vehiclePickupLocation=vehiclePickup.RentVehicle_DropLocation
    else:
        vehicle = Vehicle.objects.get(Vehicle_license_plate=Vehicle_license_plate)
        vehiclePickupLocation = vehicle.Vehicle_initial_location
# ----------------------------

    no_of_pending_request=count_pending_rent_request()

    if RentVehicle_Date_of_Booking < date.today():
        Incorrect_dates = "Please give proper dates"
        return render(request,'Owner_showdetails.html',{'Incorrect_dates':Incorrect_dates,'vehicle':vehicle,'manager':manager,'no_of_pending_request':no_of_pending_request})

    if RentVehicle_Date_of_Return < RentVehicle_Date_of_Booking:
        Incorrect_dates = "Please give proper dates"
        return render(request,'Manager_showdetails.html',{'Incorrect_dates':Incorrect_dates,'vehicle':vehicle,'manager':manager,'no_of_pending_request':no_of_pending_request})
    
    days=(RentVehicle_Date_of_Return-RentVehicle_Date_of_Booking).days+1
    total=days*vehicle.Vehicle_price
    
    rent_data = {"RentVehicle_Date_of_Booking":RentVehicle_Date_of_Booking, "RentVehicle_Date_of_Return":RentVehicle_Date_of_Return,"days":days, "total":total}

    for rv in rentvehicle:

        # if (RentVehicle_Date_of_Booking < rv.RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return < rv.RentVehicle_Date_of_Booking) or (RentVehicle_Date_of_Booking > rv.RentVehicle_Date_of_Return and RentVehicle_Date_of_Return > rv.RentVehicle_Date_of_Return):
        #     Available = True
        #     return render(request,'Manager_showdetails.html',{'Available':Available,'vehicle':vehicle,'manager':manager,'rent_data':rent_data,'no_of_pending_request':no_of_pending_request})

        if (rv.RentVehicle_Date_of_Booking >= RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return >= rv.RentVehicle_Date_of_Booking) or (RentVehicle_Date_of_Booking >= rv.RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return <= rv.RentVehicle_Date_of_Return) or (RentVehicle_Date_of_Booking <= rv.RentVehicle_Date_of_Return and RentVehicle_Date_of_Return >= rv.RentVehicle_Date_of_Return):
            if rv.isAvailable:
                Available = True
                Message = "Note that somebody has also requested for this vehicle from " + str(rv.RentVehicle_Date_of_Booking) + " to " + str(rv.RentVehicle_Date_of_Return)
                return render(request,'Manager_showdetails.html',{'Message':Message,'Available':Available,'vehicle':vehicle,'manager':manager,'rent_data':rent_data,'no_of_pending_request':no_of_pending_request})

            NotAvailable = True
            return render(request,'Manager_showdetails.html',{'NotAvailable':NotAvailable,'dates':rv,'vehicle':vehicle,'manager':manager,'no_of_pending_request':no_of_pending_request})
    
    Available = True
    return render(request,'Manager_showdetails.html',{'Available':Available,'vehicle':vehicle,'manager':manager,'rent_data':rent_data,'no_of_pending_request':no_of_pending_request,'vehiclePickupLocation':vehiclePickupLocation, 'RentVehicle_DropLocation':RentVehicle_DropLocation})

def RentRequest(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)

    rentvehicle = RentVehicle.objects.all()
    no_of_pending_request=count_pending_rent_request()
    return render(request,'Manager_RentRequest.html',{'manager':manager,'rentvehicle':rentvehicle,'no_of_pending_request':no_of_pending_request})

def SentRequests(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)

    no_of_pending_request=count_pending_rent_request()
    
    rentvehicle = RentVehicle.objects.filter(customer_email=manager_email)
    if rentvehicle.exists():
        vehicle = Vehicle.objects.all()
        return render(request,'Manager_SentRequests.html',{'manager':manager,'rentvehicle':rentvehicle,'vehicle':vehicle,'no_of_pending_request':no_of_pending_request})
    else:
        Message = "You haven't rented any vehicle yet!!"
        return render(request,'Manager_SentRequests.html',{'manager':manager,'rentvehicle':rentvehicle,'Message':Message,'no_of_pending_request':no_of_pending_request})

def count_pending_rent_request():
    no_of_pending_request=0
    rentvehicle = RentVehicle.objects.all()
    for rv in rentvehicle:
        if rv.request_status == "Pending":
            no_of_pending_request+=1
    return no_of_pending_request

def bike_list(request):
    Vehicle_type = request.GET.get('Vehicle_type', None)
    companyname = request.GET.get('companyname', None)
    Vehicle_fuel = request.GET.get('Vehicle_fuel', None)
    price_range = request.GET.get('price_range', None)

    vehicle = Vehicle.objects.all()
    if Vehicle_type:
        vehicle = vehicle.filter(Vehicle_type=Vehicle_type)
    
    if companyname:
        vehicle =vehicle.filter(Vehicle_company=companyname)

    if Vehicle_fuel:
        vehicle =vehicle.filter(Vehicle_fuel=Vehicle_fuel)

    if price_range== '500':
        vehicle = vehicle.filter(Vehicle_price__lt=500)
    elif price_range== '1000':
        vehicle = vehicle.filter(Vehicle_price__gte=500,Vehicle_price__lt=1000)
    elif price_range== '1500':
        vehicle = vehicle.filter(Vehicle_price__gte=1000,Vehicle_price__lt=1500)
    elif price_range== '2000':
        vehicle = vehicle.filter(Vehicle_price__lt=2000,Vehicle_price__gte=1500)
    elif price_range== '2500':
        vehicle = vehicle.filter(Vehicle_price__gte=2000)
    
    Message="Filters Applied!!"
    context={'vehicle':vehicle,'Message':Message}
    return render(request,'Manager_index.html',context)
