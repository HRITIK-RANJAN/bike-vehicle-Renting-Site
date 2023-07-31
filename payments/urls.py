from django.urls import path
from . import views
from CustomerHome import views as cust_views
from django.conf.urls import include

urlpatterns = [
    path('', views.index, name="Home"),
    path('Owner/',include("Owner.urls")),
    path('Manager/',include("Manager.urls")),
    path('RentVehicle/',include("RentVehicle.urls")),
    path('Home/', cust_views.Home, name="LoggedinHome"),
]