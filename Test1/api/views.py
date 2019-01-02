from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from api.serializers import UserSerializer, GroupSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .models import User



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
        
        user=UserSerializer(request.user)
        return Response(user.data, status=status.HTTP_200_OK)
    
    
    
    

    