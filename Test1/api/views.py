from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from api.serializers import UserSerializer, GroupSerializer, UserProfileSerializer,\
    DriverProfileSerializer, ShortDriverProfileSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .models import User
from django.db.models.query import QuerySet
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK,\
    HTTP_401_UNAUTHORIZED
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
import requests


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

        
        

class Flights(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def post(self, request, format=None):
        '''If the user adds a flight, then we need to check if a flight with the 
        correct flight number, destination and arrival times already exists.
        If not then we'll get the flight data from a remote api'''
        
        
        #first we want to see if the data is in the database
        flightdata= request.data
        query_set = Flights.objects.all
        
        '''json input data should be formatted as
            {
            "flight_number":"somenumber"
            "departuew_airport":"someplace"
            "departure_date": "YYYY-MM-DD",
            }'''
        
        #work out weather we have a flight with the provided data
        
        query_set=
    
        
    
    
