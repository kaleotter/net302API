'''
Created on 6 Nov 2018

@author: clini
'''


from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Car, Flight, Job, User


class UserSerializer (serializers.ModelSerializer):
    
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    
    password = serializers.CharField(min_length=8)
    address_1 = serializers.CharField(max_length=60)
        
    
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['password'], validated_data['address_1'])
            
        return user
        
    class Meta:
        model= User
        fields=('email','first_name','last_name', 'password','address_1')
        

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)
        
    
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
    
class userProfileSerializer (serializers.ModelSerializer):
    model = User
    
    id = serializers.IntegerField(read_only=True)
    address_1 = serializers.CharField(max_length=100)
    address_2 = serializers.CharField(max_length=100)
    address_3 = serializers.CharField(max_length=100)
    postcode = serializers.CharField(max_length=10)