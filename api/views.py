from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend


class UserCrud(viewsets.ModelViewSet):
    '''Class To perform CRUD api operations'''

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'city']         # To filter via name and city, http://127.0.0.1:8000/api/user/?name=Victor%20Brown&city=Bokaro
    # filterset_fields = ['city']               # http://127.0.0.1:8000/api/user/?city=Birmingham

