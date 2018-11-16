from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.


class Profile (models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    address_1=models.CharField(max_length=60)
    address_2=models.CharField(max_length=60)
    address_3=models.CharField(max_length=60)
    postcode = models.CharField(max_length=8)
    is_driver = models.BooleanField(default=False)
    drivers_licence_number = models.CharField(max_length=30)
    taxi_licence_number=models.CharField(max_length=30)
    driver_photo=models.ImageField()
    
    @receiver(post_save, sender=User)
    def create_profile (sender, instance, created, **kwargs):
        if created:
            profile.objects.create(user=instance)
            
    @receiver(post_save, sender=User)
    def update_profile(sender, instance, **kwargs):
        instance.profile.save()
    
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
    origin = models.CharField(max_length=100, null=False)
    origin_terminal = models.CharField(max_length=5, null=False)
    origin_IATA = models.CharField(max_length=5, null=False)
    destination = models.CharField(max_length=100, null=False)
    destination_terminal=models.CharField(max_length=5, null=False)
    destination_IATA = models.CharField(max_length=5, null=False)
    departure = models.DateTimeField(null=False)
    arrival = models.DateTimeField(null=False)
    
class Job (models.Model): 
    driver_id = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_id=models.ForeignKey(User, on_delete=models.CASCADE)
    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE)
    pickup_time = models.DateTimeField(null=False)
    direction= models.BooleanField(null=False) #1 for a pickup and 2 for a drop-off
    distance= models.DecimalField() #distance in miles/km? 
    subtotal= models.DecimalField() #Probably (distance*Price per distance unit*)+booking fee+extras
    total = models.DecimalField() #probably (subtotal+Taxes as applicable) 
    
    
        