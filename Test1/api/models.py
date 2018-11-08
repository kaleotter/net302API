from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Driver (models.Model):
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    driver_id = models.AutoField(primary_key=True)
    driver_name = models.CharField(max_length=150)
    car_model = models.CharField(max_length=100)
    car_colour = models.CharField(max_length=50)
    number_plate = models.CharField(max_length=10)
    
class Flight (models.Model):
    flight_id=models.CharField(max_length=10, primary_key=True)
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
    
    
        