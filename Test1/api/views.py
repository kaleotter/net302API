from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from api.serializers import UserSerializer, GroupSerializer, UserProfileSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .models import User
from django.db.models.query import QuerySet
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.parsers import JSONParser



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
        
        
                
        
        
class SingleDriver (APIView):
    print ("nothing here yet")
    
    
    
    
class ManyDrivers (APIView):
    print ("nothing here yet")

        
        

    
    
        
    

    