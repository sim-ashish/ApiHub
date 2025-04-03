from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class UserCrud(viewsets.ModelViewSet):
    '''Class To perform CRUD api operations on CustomUser Model'''

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'city']         # To filter via name and city, http://127.0.0.1:8000/api/user/?name=Victor%20Brown&city=Bokaro
    # filterset_fields = ['city']               # http://127.0.0.1:8000/api/user/?city=Birmingham


# class POSTCrud(viewsets.ModelViewSet):
#     '''Class To perform CRUD api operations on Posts Model'''

#     queryset = 'queryset for post model'
#     serializer_class = 'serializer class'
#     filter_backends = [SearchFilter]
#     search_fields = ['name', 'city']         # To filter via name or city, http://127.0.0.1:8000/api/user/?search=Victor
#     search_fields = ['^content']   # Content starts with, = exact match, $ regex



# class POSTCrud(viewsets.ModelViewSet):
#     '''Class To perform CRUD api operations on Posts Model'''

#     queryset = 'queryset for post model'
#     serializer_class = 'serializer class'
#     filter_backends = [OrderingFilter]
#     ordering_fields = ['name', 'city']  # Default is '__all__'         # To filter via name or city, http://127.0.0.1:8000/api/user/?ordering=name
#     ordering_fields = ['name']   # Content starts with, = exact match, $ regex