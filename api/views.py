from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class UserCrud(viewsets.ModelViewSet):
    '''Class To perform CRUD api operations on CustomUser Model'''

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'city']         # To filter via name and city, http://127.0.0.1:8000/api/user/?name=Victor%20Brown&city=Bokaro
    # filterset_fields = ['city']               # http://127.0.0.1:8000/api/user/?city=Birmingham


class POSTCrud(viewsets.ModelViewSet):
    '''Class To perform CRUD api operations on Posts Model'''

    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['id', 'user']    # To filter via id or userid, http://127.0.0.1:8000/api/user/?user=1
    search_fields = ['id', '$content']         # To filter via name or city, http://127.0.0.1:8000/api/user/?search=3    , http://127.0.0.1:8000/api/post/?search=nature
    # search_fields = ['^content']   # Content starts with, = exact match, $ regex



# class POSTCrud(viewsets.ModelViewSet):
#     '''Class To perform CRUD api operations on Posts Model'''

#     queryset = 'queryset for post model'
#     serializer_class = 'serializer class'
#     filter_backends = [OrderingFilter]
#     ordering_fields = ['name', 'city']  # Default is '__all__'         # To filter via name or city, http://127.0.0.1:8000/api/user/?ordering=name
#     ordering_fields = ['name']   # Content starts with, = exact match, $ regex