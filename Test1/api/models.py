from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core import mail
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.models import User, BaseUserManager, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from .UserManager import UserManager
from django.core.mail import send_mail


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    title =models.CharField(_('Title'), max_length=100, null=True,  blank=True)
    first_name=models.CharField(_('first name(s)'), max_length=100, blank =True)
    last_name=models.CharField(_('last name'), max_length=100, blank = True)
    is_active=models.BooleanField(_('account active'), default=False)
    is_driver = models.BooleanField(_('driver status'), default=False)
    is_staff = models.BooleanField(_('staff status'), default =False)
    is_admin = models.BooleanField(_('admin status'), default =False)
    
    dob = models.DateField(auto_now_add= True, blank=True)
    address_1=models.CharField(_('address line 1'),max_length=60, null=False, blank=False)
    address_2=models.CharField(_('address line 2'),max_length=60, null=True, blank=True)
    address_3=models.CharField(_('address line 3'),max_length=60, null=True, blank=True)
    city = models.CharField(_('city'),max_length=60, null=False, blank=False)
    county = models.CharField(_('county'),max_length=60, null=False, blank=False)
    postcode = models.CharField(_('postcode'),max_length=20, blank=False, null=False)
    phone_no = models.CharField(_('phone number'),max_length=50, null=True, blank=True)
    mobile_no = models.CharField(_('mobile Number'),max_length=50,null=False, blank=False)
    drivers_licence_number = models.CharField(max_length=30, null=True, blank=True)
    taxi_licence_number=models.CharField(max_length=30, null=True, blank=True)
    driver_photo=models.ImageField(blank=True)
    date_joined=models.DateTimeField(auto_now_add=True, blank=True)
    last_update=models.DateTimeField(auto_now_add=True, blank=True)
    
    objects=UserManager()
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['title', 'first_name', 'last_name','address_1','postcode','city','county','mobile_no']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural=('users')
    
    def get_full_name(self):
        """
        return the first_name and last_name formatted with a space
        """
        
        full_name = '%s %s' % (self.first_name, self.last_name)
        
        return full_name
        
        
    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        sends an email to the user
        """
        
        send_mail(subject, message, from_email, [self.email], **kwargs)


  
class Car (models.Model):
    driver_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    colour = models.CharField(max_length=50)
    number_plate = models.CharField(max_length=10)
    max_passengers= models.IntegerField()
    #photo=models.ImageField()
    
    year_of_manufacture = models.IntegerField()
    insurance_policy = models.CharField(max_length=50)
    expiry_date = models.DateField()
    

    
'''class Flight (models.Model):
    flight_number=models.CharField(max_length=10)
    origin = models.CharField(max_length=100, null=False)
    origin_IATA = models.CharField(max_length=5, null=False)
    destination = models.CharField(max_length=100, null=False)
    destination_terminal=models.CharField(max_length=5, null=False)
    destination_IATA = models.CharField(max_length=5, null=False)
    departure = models.DateTimeField(null=False)
    arrival = models.DateTimeField(null=False)'''
    
    
class Booking (models.Model): 
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True, related_name='driver_bookings')
    customer=models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_bookings')
    flight_IATA = models.CharField (max_length=10, blank=False)
    departure_ap_code = models.CharField(max_length=4, blank=False)
    arrival_ap_code = models.CharField(max_length=4, blank=False)
    flight_departure = models.DateTimeField(null=True)
    flight_arrival = models.DateTimeField(null=True)
    pickup_time = models.DateTimeField(null=False)
    booking_type = models.BooleanField(default=False) #if 0 then this is a dropoff at an airport, if 1 then it is a pickup from an airport
    pickup_lat = models.FloatField()
    pickup_long = models.FloatField()
    dropoff_lat = models.FloatField()
    dropoff_long = models.FloatField()
    booking_number = models.CharField(max_length=8)
    number_of_passengers = models.IntegerField( default=0)
    distance= models.FloatField(blank = True, null=True) #distance in miles/km? 
    subtotal= models.FloatField(blank = True, null=True) #Probably (distance*Price per distance unit*)+booking fee+extras
    total = models.FloatField(blank = True, null=True) #probably (subtotal+Taxes as applicable)
    driver_lat = models.FloatField(blank=True)
    driver_long=models.FloatField(blank=True)
    job_status=models.SmallIntegerField(default =0)