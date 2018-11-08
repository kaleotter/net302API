from django.shortcuts import render
from django.contrib.auth.models import User,Group
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer



# Create your views here.



class UserViewSet (viewsets.ModelViewSet):
    """
    Api endpoint for viewing or editing a user
    """
    queryset= User.objects.all().order_by('-date_joined')
    serializer_class= UserSerializer
    

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing or editing groups
    """
   
    queryset=Group.objects.all()
    serializer_class=GroupSerializer 

