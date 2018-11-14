from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Driver (models.Model):
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    driver_id = models.AutoField(primary_key=True)



class Profile (models.Model):
    user_id = models.OneToOneField(User, on_Delete=models.CASCADE)
    dob = models.DateField()
    address_1=models.CharField(max_length=60)
    address_2=models.CharField(max_length=60)
    address_3=models.CharField(max_length=60)
    postcode = models.CharField(max_length=8)
    is_driver = models.BooleanField(default=False)
    drivers_licence_number = models.CharField(max_length=30, null=False)
    taxi_licence_number=models.CharField(max_length=30, null =False)
    driver_photo=models.ImageField(null=False)
    
class Car (models.Model):
    model = models.CharField(max_length=100)
    colour = models.CharField(max_length=50)
    number_plate = models.CharField(max_length=10)
    max_passengers= models.IntegerField()
    photo=models.ImageField()
    
    year_of_manufacture = models.DateField()
    insurance_policy = models.CharField(max_length=50)
    expiry_date = models.DateField()
    

    
class Flight (models.Model):
    flightnumber=models.CharField(max_length=10)
    flight_origin = models.CharField(max_length=100, null=False)
    flight_origin_IATA = models.CharField(max_length=5, null=False)
    flight_destination = models.CharField(max_length=100, null=False)
    flight_destination_IATA = models.CharField(max_length=5, null=False)
    flight_departure = models.DateTimeField(null=False)
    flight_arrival = models.DateTimeField(null=False)
    current_eta = models.DateTimeField(null=False)
    
class Job (models.Model):
    # customer_id = 
    driver_id = models.ForeignKey(Driver.driver_id, on_delete=models.CASCADE)
    flight_id = models.ForeignKey(Flight.flight_id, on_delete=models.CASCADE)
    pickup_time = models.DateTimeField(null=False)
    direction= models.BooleanField(null=False) #1 for a pickup and 2 for a drop-off
    distance= models.DecimalField() #distance in miles/km? 
    subtotal= models.DecimalField() #Probably (distance*Price per distance unit*)+booking fee+extras
    total = models.DecimalField() #probably (subtotal+Taxes as applicable) 
    
    
        