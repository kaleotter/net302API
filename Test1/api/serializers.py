'''
Created on 6 Nov 2018

@author: clini
'''


from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Car, Driver, Flight, Job


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model= User
        fields=('username','email','first_name','last_name',)
        
        
        
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)
        
        


        