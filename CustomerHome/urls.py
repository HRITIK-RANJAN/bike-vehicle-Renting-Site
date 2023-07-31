from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from payments import views as cust_views

urlpatterns = [
    path('', views.index, name="Home"),
    path('Home/', views.Home, name="LoggedinHome"),
    path('signin/',views.signin,name="SignIn"),
    path('Logout/',views.Logout,name="Logout"),
    path('register/',views.register,name="Register"),
    path('Profile/',views.Profile,name="Profile"),
    path('about/', views.about_us, name="AboutUs"),
    path('contact/', views.contact_us, name="ContactUs"),
    path('search/', views.search, name="Search"),
    path('LoginAuthentication/',views.LoginAuthentication,name="LoginAuthentication"),
    path('RegisterCustomer/',views.RegisterCustomer,name="RegisterCustomer"),
    path('VehicleDetails/<str:Vehicle_license_plate>/',views.showdetails,name="VehicleDetails"),
    path('CheckAvailability/<str:Vehicle_license_plate>/',views.CheckAvailability,name="CheckAvailability"),
    path('SentRequests/',views.SentRequests,name="SentRequests"),
    path('RentVehicle/',include("RentVehicle.urls")),
    path('Owner/',include("Owner.urls")),
    path('Manager/',include("Manager.urls")),
    path('payments/',include("payments.urls")),
    path('completePayment/<str:RentVehicle_Date_of_Booking>/',cust_views.completePayment, name="completePayment"),
    path('bike_list/',views.bike_list,name="bike_list"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)