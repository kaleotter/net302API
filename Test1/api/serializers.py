'''
Created on 6 Nov 2018

@author: clini
'''


from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Car, Flight, Job, Profile


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model= User
        fields=('username','email','first_name','last_name',)
        
        
        
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)
        
        


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        id = serializers.IntegerField(read_only=True)
        user_id = serializers.IntegerField()
        dob = serializers.DateField(required=True)
        address_1 = serializers.CharField(max_length=60)
        address_2 = serializers.CharField(max_length=60)
        address_3 = serializers.CharField(max_length=60)
        postcode = serializers.CharField(max_length=10)
        is_driver =serializers.BooleanField()
        drivers_licence_number= serializers.CharField(max_length=30)
        taxi_licence_number=serializers.CharField(max_length=30)
        driver_photo= serializers.ImageField
        
    def create(self, validated_data):
        """
        Create and return a new User Profile instance, given correctly validated data
        (NB, we shouldn't need this normally, but there might be some edge cases where a profile needs to be manually created.)
        """
        
        return Profile.objects.create(**validated_data)
    
    def updateCustomer(self, instance, validated_data):
        """
        Update and return an existing Profile instance, given correctly Validated data
        """
        
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.address_1 = validated_data.get('address_1', instance.address_1)
        instance.address_2 = validated_data.get('address_2', instance.address_2)
        instance.address_3 = validated_data.get('address_3', instance.address_3)
        instance.postcode = validated_data.get('postcode', instance.postcode)
        
        instance.save()
        return instance
        
    def updateDriver(self,instance, validated_data):
        """
        updates and returns an existing profile, additionally using the fields for a valid driver.
        """
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.address_1 = validated_data.get('address_1', instance.address_1)
        instance.address_2 = validated_data.get('address_2', instance.address_2)
        instance.address_3 = validated_data.get('address_3', instance.address_3)
        instance.postcode = validated_data.get('postcode', instance.postcode)
        instance.is_driver = validated_data.get('is_driver', instance.is_driver)
        instance.drivers_licence_number=validated_data.get('drivers_licence',instance.drivers_licence_number)
        instance.taxi_licence_number=validated_data.get('taxi_licence'), instance.taxi_licence_number
        
        
        instance.save()
        return instance
    
    
class FlightSerializer(serializers.ModelSerializer):
    model=Flight
        
    id = serializers.IntegerField(read_only=True)
    flight_number = serializers.CharField(max_length=10)
    origin_airport = serializers.CharField(max_length=100)
    origin_IATA = serializers.CharField(max_length=10)
    origin_terminal = serializers.CharField(max_length=5)
    destination = serializers.CharField(max_length=100)
    destination_terminal = serializers.CharField(max_length=5)
    destination_IATA = serializers.CharField(max_length=10)
    departure = serializers.DateTimeField()
    arrival = serializers.DateTimeField()
        
    def create(self, validated_data):
        """
        Create and return a new User Flight instance, given correctly validated data
        """
            
        return Flight.objects.create()
       
    def update (self, instance, validated_data):
        """
        Update and return an existing Flight instance, given correctly Validated data
        """
        instance.flight_number = validated_data.get('flight_number'),instance.flight_number
        instance.origin_airport = validated_data.get('origin_airport'),instance.origin_airport
        instance.origin_IATA = validated_data.get('origin_IATA'),instance.origin_IATA
        instance.origin_terminal = validated_data.get('origin_terminal'),instance.origin_terminal
        instance.destination = validated_data.get('destination'),instance.destination
        instance.destination_terminal = validated_data.get('destination_terminal'),instance.destination_terminal
        instance.destination_IATA = validated_data.get('destination_iata'), instance.destination
        instance.departure = validated_data.get('departure'), instance.departure
        instance.arrival = validated_data.get('arrival'), instance.arrival
        
        instance.save()
        return instance
