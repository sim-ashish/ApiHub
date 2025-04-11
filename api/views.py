from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from api.throttling import CustomThrottle
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.core.cache import cache
import re
import json
from django_redis import get_redis_connection

class UserCrud(viewsets.ModelViewSet):
    '''Class To perform CRUD api operations on CustomUser Model'''

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    throttle_classes = [CustomThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'city']         # To filter via name and city, http://127.0.0.1:8000/api/user/?name=Victor%20Brown&city=Bokaro
    # filterset_fields = ['city']               # http://127.0.0.1:8000/api/user/?city=Birmingham


class POSTCrud(viewsets.ModelViewSet):
    '''Class To perform CRUD api operations on Posts Model'''
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    throttle_classes = [CustomThrottle]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['id', 'user']    # To filter via id or userid, http://127.0.0.1:8000/api/user/?user=1
    search_fields = ['id', '$content']         # To filter via name or city, http://127.0.0.1:8000/api/user/?search=3    , http://127.0.0.1:8000/api/post/?search=nature
    # search_fields = ['^content']   # Content starts with, = exact match, $ regex



################################### Custom Api Views ############################

class CustomAPIViewSet(viewsets.ModelViewSet):
    '''Class To create and show Custom Api's with name , endpoint, status_codes and validations'''
    serializer_class = CustomApiSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # return CustomApi.objects.filter(user=self.request.user, public = True)
        return CustomApi.objects.filter(user=self.request.user)

    
    def perform_create(self, serializer):                   # ModelViewSet create method
        serializer.save(user=self.request.user)



class DynamicApiHandler(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, endpoint, data_id=None):
        try:
            custom_api = CustomApi.objects.get(endpoint=endpoint)
        except CustomApi.DoesNotExist:
            return Response({"error": "Endpoint not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if data_id:
            try:
                # record = APIData.objects.get(api=custom_api, id=data_id)
                # serializer = APIDataSerializer(record)
                # return Response(serializer.data, status = status.HTTP_200_OK)
                record = APIData.objects.get(api=custom_api, data__id = data_id)
                return Response(record.data, status = status.HTTP_200_OK)
            
            except APIData.DoesNotExist:
                return Response({"error": "Data not found for this ID"}, status=status.HTTP_404_NOT_FOUND)
        else:
            records = APIData.objects.filter(api=custom_api).order_by('created_at')
            # print(records.values('data'))
            # records = APIData.objects.filter(api=custom_api, data__id = 1).order_by('-created_at')
            # print("QUERY RESULT", records.values('data'))

            # serializer = APIDataSerializer(records, many=True)
            # return Response(serializer.data, status = status.HTTP_200_OK)
            return Response({"data": [r.data for r in records]}, status = status.HTTP_200_OK)

    def post(self, request, endpoint):
        try:
            custom_api = CustomApi.objects.get(endpoint=endpoint)
        except CustomApi.DoesNotExist:
            return Response({"error": "Endpoint not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            data = request.data           
            print("DATA : ", data)
        except Exception:
            return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
        
        validations = custom_api.validations or {}

        api_fields = set(validations.keys())
        data_fields = set(data.keys())

        if len(data_fields - api_fields) != 0:
                return Response({"error": f'{data_fields - api_fields}, is/are extra fields'}, status=status.HTTP_400_BAD_REQUEST)

        for field, rules in validations.items():
            if not rules.get("optional") and field not in data:
                return Response({"error": f"Missing required field: {field}"}, status=status.HTTP_400_BAD_REQUEST)

            if field in data:
                value = data[field]
                if rules.get("type") == "integer":
                    if not isinstance(value, int):
                        return Response({"error": f"{field} must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
                    if "min" in rules and value < rules["min"]:
                        return Response({"error": f"{field} must be >= {rules['min']}"}, status=status.HTTP_400_BAD_REQUEST)
                    if "max" in rules and value > rules["max"]:
                        return Response({"error": f"{field} must be <= {rules['max']}"}, status=status.HTTP_400_BAD_REQUEST)

                if rules.get("type") == "decimal":
                    if not isinstance(value, float):
                        return Response({"error": f"{field} must be a decimal"}, status=status.HTTP_400_BAD_REQUEST)
                    if "min" in rules and value < rules["min"]:
                        return Response({"error": f"{field} must be >= {rules['min']}"}, status=status.HTTP_400_BAD_REQUEST)
                    if "max" in rules and value > rules["max"]:
                        return Response({"error": f"{field} must be <= {rules['max']}"}, status=status.HTTP_400_BAD_REQUEST)

                if rules.get("type") == "string":
                    if not isinstance(value, str):
                        return Response({"error": f"{field} must be a string"}, status=status.HTTP_400_BAD_REQUEST)
                    if "min_length" in rules and len(value) < rules["min_length"]:
                        return Response({"error": f"{field} length must be >= {rules['min_length']}"}, status=status.HTTP_400_BAD_REQUEST)
                    if "max_length" in rules and len(value) > rules["max_length"]:
                        return Response({"error": f"{field} length must be <= {rules['max_length']}"}, status=status.HTTP_400_BAD_REQUEST)
                    if "regex" in rules:
                        if not re.match(rules["regex"], value):
                            return Response({"error": f"{field} is not in the correct format"}, status=status.HTTP_400_BAD_REQUEST)

                if rules.get("type") == "boolean":
                    if not isinstance(value, bool):
                        return Response({"error": f"{field} must be a Boolean"}, status=status.HTTP_400_BAD_REQUEST)

        # Getting id to uniquely identify data from redis or db, if validation success!!
        api_id = cache.get(str(endpoint), None)
        if api_id is None:
            api_id = int(custom_api.auto_id)
            cache.set(str(endpoint), api_id, timeout= 60 * 60 *24)      # storing for 24 hrs

        # # Save data if valid
        data['id'] = api_id
        APIData.objects.create(api=custom_api, data=data)
        cache.set(str(endpoint), api_id + 1, timeout= 60 * 60 *24)            # Increasing the id for that specific endpoint
        return Response(custom_api.success_response, status=status.HTTP_201_CREATED)
    
    def put(self, request, endpoint, data_id=None): 
        pass
  
    def patch(self, request, endpoint, data_id=None): 
        pass
          
    def delete(self, request, endpoint, data_id=None): 
        try:
            custom_api = CustomApi.objects.get(endpoint=endpoint)
        except CustomApi.DoesNotExist:
            return Response({"error": "Endpoint not found"}, status=status.HTTP_404_NOT_FOUND)
        if data_id:
            try:
                record = APIData.objects.get(api=custom_api, data__id = data_id)
                record.delete()
                return Response(custom_api.success_response, status = status.HTTP_204_NO_CONTENT)
            
            except APIData.DoesNotExist:
                return Response(custom_api.error_response, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Method Not Allowed!"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)