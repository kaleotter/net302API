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


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name=models.CharField(_('first name'), max_length=100, blank =True)
    last_name=models.CharField(_('last name'), max_length=100, blank = True)
    is_active=models.BooleanField(_('account active'), default=False)
    is_driver = models.BooleanField(_('driver status'), default=False)
    is_staff = models.BooleanField(_('staff status'), default =False)
    is_admin = models.BooleanField(_('admin status'), default =False)
    
    dob = models.DateField(auto_now_add= True, blank=True)
    address_1=models.CharField(_('address line 1'),max_length=60, blank=True)
    address_2=models.CharField(_('address line 2'),max_length=60, blank=True)
    address_3=models.CharField(_('address line 3'),max_length=60, blank=True)
    city = models.CharField(_('city'),max_length=60, blank=True)
    county = models.CharField(_('county'),max_length=60, blank=True)
    postcode = models.CharField(_('postcode'),max_length=8, blank=True)
    drivers_licence_number = models.CharField(max_length=30, blank=True)
    taxi_licence_number=models.CharField(max_length=30, blank=True)
    driver_photo=models.ImageField(blank=True)
    date_joined=models.DateField(auto_now_add=True, blank=True)
    last_update=models.DateField(auto_now_add=True, blank=True)
    
    objects=UserManager()
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural=('users')
    
    def get_full_name(self):
        """
        return the first_name and last_name formatted with a space
        """
        
        full_name = '%s %s' % (self.first_name, self.last_name)
        
        
    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        sends an email to the user
        """
        
        send_mail(subject, message, from_email, [self.email], **kwargs)


  
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
    driver_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver')
    customer_id=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')
    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE)
    pickup_time = models.DateTimeField(null=False)
    direction= models.BooleanField(null=False) #1 for a pickup and 2 for a drop-off
    distance= models.FloatField() #distance in miles/km? 
    subtotal= models.FloatField() #Probably (distance*Price per distance unit*)+booking fee+extras
    total = models.FloatField() #probably (subtotal+Taxes as applicable) 
    
    
        