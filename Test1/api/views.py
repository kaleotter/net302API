from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from api.serializers import UserSerializer, GroupSerializer, UserProfileSerializer,\
    DriverProfileSerializer, ShortDriverProfileSerializer, BookingSerializer,\
    CarSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .models import *
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK,\
    HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action, permission_classes
import requests
from api.helpers import RandomStringGen, GMapsAddressConverter


# Create your views here.


class UserList (generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset= User.objects.all()
    serializer_class=UserSerializer
    
    
class UserDetails(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset=User.objects.all()
    serializer_class= UserSerializer
    
class GroupList(generics.ListAPIView):
    permission_classes=[permissions.IsAuthenticated, TokenHasScope]
    required_scopes=['groups']
    queryset = Group.objects.all()
    serializer_class=GroupSerializer
    

    

class RegisterUser(APIView):
    permission_classes=[permissions.AllowAny]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        
        #check if serialized data is valid
        if serializer.is_valid():
            user = serializer.save()
            
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

class UpdateProfile(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def post(self, request, format=None):
        
        user=request.user
        print (user.id)
        try:
            query_set=User.objects.get(pk=user.id)
            print (user.id)
            print (user.address_1)
            print (user.postcode)
        except User.DoesNotExist:
            return Response("no user found", status=HTTP_404_NOT_FOUND)
            
        print("we got a queryset")
        
        
        data=request.data
        print("we got data")
        print(data)
        
        serializer=UserProfileSerializer(request.user, data=data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response("Yay we did it!", HTTP_200_OK )
        
        else:
            return Response(serializer.errors)
        
        
class SingleUser(APIView):
    
    permission_classes=(permissions.IsAuthenticated)
    
    def get(self, request, userID):
        user = request.user
        
        if (user.is_staff== 1 ):
            query_set = object.User.get(pk=userID, is_driver=0)
            
            serializer = UserSerializer(query_set)
            
            return Response(serializer, HTTP_200_OK)
            
        else:
            return Response("You are not authorized to view this resource", HTTP_401_UNAUTHORIZED)
            
    
    
    
class ListUsers(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request):
        user=request.user
        search=request.query_params
        print(search)
        
        
        if(user.is_staff==1):
            query_set = User.objects.all()
            
            if ('first_name' in search): 
                
                query_set= query_set.filter(first_name__icontains=search['first_name'].strip('"'))
                            
            if('last_name' in search): 
                query_set= query_set.filter(last_name__icontains=search['last_name'].strip('"'))
            
            if('dob_before' in search):
                query_set= query_set.filter(dob__lte=search['dob'].strip('"'))
                
            if('dob_after' in search):
                query_set= query_set.filter(dob__gte=search['dob'].strip('"'))
                
            if('is_staff' in search):
                query_set= query_set.filter(is_staff__iexact=search['is_staff'].strip('"'))
                
            if('is_driver' in search):
                query_set= query_set.filter()
                            
            if query_set: #we got data
        
                serializer = UserProfileSerializer(query_set, many=True)
            
                print (serializer)
        
                return Response(serializer.data, HTTP_200_OK)
        
            else:
                return Response("no users found", HTTP_404_NOT_FOUND)
            
            
        #apply simple search filters
              
        
class SingleDriver (APIView):
    #check user permissions
    permission_classes=(permissions.AllowAny)
    
    def get (self, request, format=None):
        
        activeUser=request.user
        
        
        
        
        if (activeUser and (activeUser.is_driver==1 or activeUser.is_staff==1)): #We got a logged in user who is staff, give the full profile
            
            #just return all valid data for the driver            
            serialized = DriverProfileSerializer(activeUser)
            return Response(serialized.data, HTTP_200_OK )
        
    
            
    
    
class ManyDrivers (APIView):
    print ("nothing here yet")

        
        
    
        
    
    
class CustomerViewSet (viewsets.ViewSet):
    """
    Handles most user functions for Customers
    """    
    
    def get_permissions(self):
        
        
        if self.action =='update':
            permission_classes = [permissions.IsAuthenticated]
            
        elif self.action =='current':
            permission_classes = [permissions.IsAuthenticated] 
            
        else:
            permission_classes = [permissions.AllowAny]
    
        return [permission() for permission in permission_classes]
    
    
    def create (self, request):
        serializer = UserSerializer(data=request.data)
        
        #check if serialized data is valid
        if serializer.is_valid():
            user = serializer.save()
            
            if user:
                return Response("Your account has been created Successfully!", status=status.HTTP_201_CREATED)
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'])
    def current (self, request, pk=None):
        """get the current user profile data for an authenticated user"""
        
        user=request.user
        
        if user: #just make sure we have data for the user here
            serializer=UserProfileSerializer(user)
            
            return Response(serializer.data, HTTP_200_OK)
        
        else:
            return Response("userProfile not found", HTTP_404_NOT_FOUND)
        
    def update (self, request, pk=None):
        
        #get the authenticated user
        user=request.user
        
        data=request.data
        
        serializer = UserProfileSerializer(user, data=data)
        
        if serializer.is_valid():
            serializer.save()
            
            if user:
                return Response("user profile updated successfully", HTTP_200_OK)
            
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)

class DriverViewSet(viewsets.ViewSet):
    
    def update (self, request, pk=None):
        user=request.user 
            
        '''first check that we have a driver, if not, then we don't have an authorised
        user and we should return unauthorised'''
        
        if user.is_driver == 1:
            #serialize the data and then check that it is valid
            
            serializer = DriverProfileSerializer(user, data=request.data)
            
            if serializer.is_valid:
                #then save the updates and return message and 200
                
                serializer.save()
                
                return Response("Driver profile Successfully updated!")
            
            else: #There was a problem with the serializer, return the errors
                
                return Response(serializer.errors, HTTP_400_BAD_REQUEST)
            
        else:
            
            return Response("Unauthorised", HTTP_401_UNAUTHORIZED)
        
        
'''class StaffFunctionsViewSet (viewsets.ViewSet):
    
    
    @action(detail = True, methods=['put'])
    def activate_account(self, request, pk=None):
        
        user=request.user'''
        
        
class BookingViewSet(viewsets.ViewSet):
    
    permission_classes=[permissions.IsAuthenticated]
    
    def create (self, request):
        
        user = request.user
        
        data = request.data
        
        
        #first do the address translations
        
        pickup =GMapsAddressConverter.to_coords(data['pickup_address_1'],
                                       data['pickup_address_2'], 
                                       data['pickup_address_3'], 
                                       data['pickup_city'], 
                                       data['pickup_postcode'])
        
        if isinstance(pickup, dict):
        
            data.pop('pickup_address_1', None)
            data.pop('pickup_address_2', None)
            data.pop('pickup_address_3', None)
            data.pop('pickup_postcode', None)
            data.pop('pickup_city', None)
            
            print(data)
            
            data['pickup_lat']=pickup['lat']
            data['pickup_long']=pickup['lng']
            
        else:
            return Response(pickup, HTTP_400_BAD_REQUEST)
            
            print(data)
        dropoff = GMapsAddressConverter.to_coords(data['dropoff_address_1'], 
                                        data['dropoff_address_2'], 
                                        data['dropoff_address_3'],
                                        data['dropoff_city'],
                                        data['dropoff_postcode'])
        
        
            
        if isinstance(dropoff,dict):
        
            data.pop('dropoff_address_1', None)
            data.pop('dropoff_address_2', None)
            data.pop('dropoff_address_3', None)
            data.pop('dropoff_postcode', None)
            data.pop('dropoff_city', None)
            
            data['dropoff_lat']=dropoff['lat']
            data['dropoff_long']=dropoff['lng']   
        
        
        else:
            return Response('problem connecting to google api', HTTP_400_BAD_REQUEST)
        
        # now generate booking code
        
        data['booking_number'] = RandomStringGen.generate()
        
        #apply userid to customerid
        data['customer'] = user.id 
        data['driver'] = user.id
        
        print("here is the data")
        print (data)
        print(" ")
        
        #now serialize the data
        serializer = BookingSerializer(data=data)
        
        if serializer.is_valid():
            print(serializer.validated_data)
            
            serializer.save()
            
            return Response('booking created successfully', HTTP_200_OK)
        
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        '''get a booking with a specific customer and driver'''
        
        user = request.user
        
        booking = Booking.objects.get(id=pk)
        
        #serialize the booking
        serializer = BookingSerializer(booking, Many=False)
        
        return Response(serializer, HTTP_200_OK)
    
    def list (self, request):
        
        user=request.user
        
        data=Booking.objects.all()
        search=request.query_params
        #now we can filter the results
        
        if search['job_search']==0:
            #we know we're looking for accepted jobs
            
            data=data.filter(driver__exact=user.id)
            
        
        
        serializer = BookingSerializer(data, many=True)
        
        
        return Response(serializer.data, HTTP_200_OK)
        
        
class CarViewSet (viewsets.ViewSet):
    permission_classes =[permissions.IsAuthenticated]
    
    def create(self, request):
    
        user = request.user
        data = request.data
    
        if user.is_driver == 1:
    
            #add driver_id to the data
            data['driver_id']= user.id
            
            print("here is the data")
            print (data)
            print(" ")
            #serialize the data
            serializer = CarSerializer(data=data)
        
            
        
            if serializer.is_valid():
            
                print(serializer.validated_data)
                serializer.save()
                return Response("car added to database!", HTTP_200_OK)
                
            else:
                
                return Response(serializer.errors, HTTP_400_BAD_REQUEST)
        
        else:
            return Response('user not authorized', HTTP_401_UNAUTHORIZED)
        
        
    def update(self, request, pk=None):
        
        user=request.user
        data =request.data
        
        #get the car to be updated
        car=Car.objects.get(id=pk)
        
        
        data['driver_id']=user.id
        
        if user.is_driver == 1:
            
            
            serializer = CarSerializer(car, data=request.data)
            
            
            if serializer.is_valid():
                
                serializer.save()
                
                return Response("car details updated successfully", HTTP_200_OK)
            
            else:
                return Response(serializer.errors, HTTP_400_BAD_REQUEST)
            
        else:
            return Response('not authorized', HTTP_401_UNAUTHORIZED)


    
