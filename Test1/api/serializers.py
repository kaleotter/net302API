'''
Created on 6 Nov 2018

@author: clini
'''


from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Car, Flight, Job, User
from datetime import datetime


class UserSerializer (serializers.ModelSerializer):
    
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    
    password = serializers.CharField(min_length=8)
    first_name=serializers.CharField(max_length=50)
    last_name=serializers.CharField(max_length=50)
    title=serializers.CharField(max_length=8)
    address_1 = serializers.CharField(max_length=60)
    dob = serializers.DateField()
    address_1 = serializers.CharField(max_length=100)
    address_2 = serializers.CharField(max_length=100)
    address_3 = serializers.CharField(max_length=100)
    postcode = serializers.CharField(max_length=10)
    county = serializers.CharField(max_length=50)
    city = serializers.CharField(max_length=50)
    phone_no = serializers.CharField()
    mobile_no = serializers.CharField()
        
    
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], 
                                        validated_data['title'],
                                        validated_data['first_name'],
                                        validated_data['last_name'],
                                        validated_data['address_1'],
                                        validated_data['postcode'],
                                        validated_data['city'],
                                        validated_data['county'],
                                        validated_data['mobile_no'],
                                        validated_data['password'],
                                        validated_data['address_2'],
                                        validated_data['address_3'],
                                        validated_data['phone_no'])
            
        return user
        
    class Meta:
        model= User
        fields=('email','title','first_name','last_name', 'password','address_1','address_2','address_3','postcode','city','county','phone_no','mobile_no','dob')
        

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
    
class UserProfileSerializer (serializers.ModelSerializer):
    model = User
    
    id = serializers.IntegerField(read_only=True)
    dob = serializers.DateField(read_only=True)
    title=serializers.CharField(max_length=8, required=True)
    first_name=serializers.CharField(max_length=80,required=True)
    last_name=serializers.CharField(max_length=80,required=True)
    address_1 = serializers.CharField(max_length=100, required=True)
    address_2 = serializers.CharField(max_length=100,required=True)
    address_3 = serializers.CharField(max_length=100,required=True)
    postcode = serializers.CharField(max_length=10, required=True)
    county = serializers.CharField(max_length=50, required=True)
    city = serializers.CharField(max_length=50, required=True)
    phone_no = serializers.CharField(required=True)
    mobile_no = serializers.CharField(required=True)


        
    
    def update (self, instance, validated_data):
        instance.title= validated_data.get('title'), instance.title
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.first_name)
        instance.address_1 = validated_data.get('address_1', instance.address_1)
        instance.address_2 = validated_data.get('address_2', instance.address_2)
        instance.address_3 = validated_data.get('address_3', instance.address_3)
        instance.postcode = validated_data.get('postcode', instance.postcode)
        instance.county = validated_data.get('county', instance.county)
        instance.phone_no = validated_data.get('phone_no',instance.phone_no)
        instance.mobile_no = validated_data.get('mobile_no', instance.mobile_no)
        instance.last_update = datetime.now()
        
        instance.save()
        return instance
        

    class Meta:
        model = User
        fields = ('id','dob','title','first_name','last_name','address_1','address_2','address_3','postcode','county','city','phone_no','mobile_no','last_update')
        
class DriverProfileSerializer (serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    first_name=serializers.CharField(max_length=80)
    last_name=serializers.CharField(max_length=80)
    drivers_licence_number = serializers.CharField(max_length=20)
    taxi_licence_number = serializers.CharField(max_length=20)
    last_update= serializers.DateTimeField()
    #driver_photo = serializers.ImageField()
    
    def update(self, instance, validated_data):
        instance.first_name=validated_data.get('first_name', instance.first_name)
        instance.last_name=validated_data.get('last_name', instance.last_name)
        instance.drivers_licence_number = validated_data.get('drivers_licence_number',instance.drivers_licence_number)
        instance.taxi_licence_number = validated_data.get('taxi_licence_number', instance.taxi_licence_number)
        instance.last_update=datetime.now()
    
    class Meta:
        Model=User
        
        fields=('id','title','first_name','last_name','drivers_licence_number','last_update')