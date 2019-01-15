'''
Created on 6 Nov 2018

@author: clini
'''


from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Car, User
from .models import Booking as BookingModel
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
        
        user.groups.add(1)
            
        return user
        
    class Meta:
        model= User
        fields=('email','title','first_name','last_name', 'password','address_1','address_2','address_3','postcode','city','county','phone_no','mobile_no','dob')
        

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)
        
    
'''class FlightSerializer(serializers.ModelSerializer):
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
    
    class Meta:
        model=Flight
        
        fields=('__all__')
        
    def create(self, validated_data):
        """
        Create and return a new User Flight instance, given correctly validated data
        """
        
        return Flight.objects.create()
       
    def update (self, instance, validated_data):
        """
        Update and return an existing Flight instance, given correctly Validated data
        """
        
        instance.flight_number = validated_data.get('flight_number',instance.flight_number)
        instance.origin_airport = validated_data.get('origin_airport',instance.origin_airport)
        instance.origin_IATA = validated_data.get('origin_IATA',instance.origin_IATA)
        instance.origin_terminal = validated_data.get('origin_terminal',instance.origin_terminal)
        instance.destination = validated_data.get('destination',instance.destination)
        instance.destination_terminal = validated_data.get('destination_terminal',instance.destination_terminal)
        instance.destination_IATA = validated_data.get('destination_iata', instance.destination)
        instance.departure = validated_data.get('departure', instance.departure)
        instance.arrival = validated_data.get('arrival', instance.arrival)
        
        instance.save()
        return instance'''
    
    
    
class UserProfileSerializer (serializers.ModelSerializer):
    model = User
    
    id = serializers.IntegerField(read_only=True)
    dob = serializers.DateField(read_only=True)
    title=serializers.CharField(max_length=8, required=False)
    first_name=serializers.CharField(max_length=80,required=False)
    last_name=serializers.CharField(max_length=80,required=False)
    address_1 = serializers.CharField(max_length=100, required=False)
    address_2 = serializers.CharField(max_length=100,required=False)
    address_3 = serializers.CharField(max_length=100,required=False)
    postcode = serializers.CharField(max_length=10, required=False)
    county = serializers.CharField(max_length=50, required=False)
    city = serializers.CharField(max_length=50, required=False)
    phone_no = serializers.CharField(required=False)
    mobile_no = serializers.CharField(required=False)


        
    
    def update (self, instance, validated_data):
        instance.title= validated_data.get('title', instance.title)
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
    
    class Meta:
        model = User
        fields=('id','title','first_name','last_name','drivers_licence_number', 'taxi_licence_number','last_update')
    
    def update(self, instance, validated_data):
        instance.title =validated_data.get('title', instance.validated_title)
        instance.first_name=validated_data.get('first_name', instance.first_name)
        instance.last_name=validated_data.get('last_name', instance.last_name)
        instance.drivers_licence_number = validated_data.get('drivers_licence_number',instance.drivers_licence_number)
        instance.taxi_licence_number = validated_data.get('taxi_licence_number', instance.taxi_licence_number)
        instance.last_update=datetime.now()
    
    
    
class ShortDriverProfileSerializer (serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    title=serializers.CharField()
    first_name=serializers.CharField(max_length=80)
    last_name=serializers.CharField(max_length=80)
    #driver_photo = serializers.ImageField()
    
    class Meta:
        model = User
        fields=('id','title','first_name','last_name','last_update')
    
    
    
class UserPermissionSerializer (serializers.ModelSerializer):
    
    id= serializers.IntegerField(read_only=True)
    is_admin= serializers.BooleanField()
    is_staff = serializers.BooleanField()
    
    class Meta:
        model = User
        fields=('id','is_admin','is_driver','is_staff','last_update')
        
        
class BookingSerializer (serializers.ModelSerializer):
    
    id = serializers.IntegerField(read_only=True)
    driver= serializers.PrimaryKeyRelatedField
    customer=serializers.PrimaryKeyRelatedField
    flight_IATA = serializers.CharField(max_length=10, required=True)
    departure_ap_code = serializers.CharField(max_length=4, required=True)
    arrival_ap_code = serializers.CharField(max_length=4, required=True)
    flight_departure = serializers.DateTimeField(required=True)
    flight_arrival = serializers.DateTimeField(required=True)
    pickup_time = serializers.DateTimeField(required=True)
    pickup_lat = serializers.FloatField(required=True)
    pickup_long = serializers.FloatField(required=True)
    dropoff_lat = serializers.FloatField(required=True)
    dropoff_long = serializers.FloatField(required=True)
    booking_number = serializers.CharField(max_length=8, required=True)
    number_of_passengers = serializers.IntegerField()
    distance = serializers.FloatField(required=False)
    subtotal = serializers.FloatField(required=False)
    total = serializers.FloatField(required=False)
    
    class Meta:
        model = BookingModel
        fields = ('__all__')
        
    def create(self, validated_data):
        
        return BookingModel.objects.create()
        
    
    def update(self, instance, validated_data):
        instance.driver =validated_data.get('driver',instance.driver)
        instance.customer_id=validated_data.get('customer', instance.customer)
        instance.flight_IATA=validated_data.get('flight_IATA',instance.flight_IATA)
        instance.departure_ap_code = validated_data.get('departure_ap_code',instance.departure_ap_code)
        instance.arrival_ap_code = validated_data.get('arrival_ap_code', instance.arrival_ap_code)
        instance.flight_departure = validated_data.get('flight_departure',instance.flight_departure)
        instance.flight_arrival = validated_data.get('flight_arrival',instance.flight_arrival)
        instance.pickup_time = validated_data.get('pickup_time',instance.pickup_time)
        instance.pickup_lat = validated_data.get('pickup_lat', instance.pickup_lat)
        instance.pickup_long = validated_data.get('pickup_long', instance.pickup_long)
        instance.dropoff_lat = validated_data.get('dropoff_lat', instance.dropoff_lat)
        instance.dropoff_long = validated_data.get('dropoff_long', instance.dropoff_long)
        instance.booking_number = validated_data.get('booking_number', instance.booking_number)
        instance.number_of_passengers = validated_data.get('number_of_passengers',instance.number_of_passengers)
        instance.distance = validated_data.get('distance', instance.distance)
        instance.subtotal = validated_data.get('subtotal', instance.subtotal)
        instance.total = validated_data.get('total', instance.total)
        
        instance.save()
        return instance
        
        
        
        
class CarSerializer (serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    driver_id = serializers.PrimaryKeyRelatedField
    model = serializers.CharField(max_length=100)
    colour = serializers.CharField(max_length=50)
    number_plate = serializers.CharField(max_length=10)
    max_passengers =serializers.IntegerField()
    #photo=serializers.ImageField()
    year_of_manufacture = serializers.IntegerField
    insurance_policy = serializers.CharField(max_length=50)
    expiry_date = serializers.DateField()

    class Meta:
        model=Car
        fields=('__all__')
        
        def create (self, validated_data):
            
            return Car.object.create()
        
        def update (self, instance, validated_data):
            
            instance.model=validated_data.get('model',instance.model)
            instance.driver_id = validated_data.get('driver_id', instance.driver_id)
            instance.colour=validated_data.get('colour', instance.colour)
            instance.number_plate=validated_data.get('number_plate', instance.number_plate)
            instance.max_passengers = validated_data.get('max_passengers', instance.max_passengers)
            #instance.photo = validated_data.get('photo', instance.photo)
            instance.year_of_manufacture = validated_data.get('year_of_manufacture',instance.year_of_manufacture)
            instance.insurance_policy = validated_data.get('insurance_policy', instance.insurance_policy)
            instance.expiry_date = validated_data.get('expiry_date', instance.expiry_date)
            
            instance.save()
            return instance
        