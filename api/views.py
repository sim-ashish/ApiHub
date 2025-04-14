from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from api.throttling import CustomThrottle
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.core.cache import cache
import re
import json
from django_redis import get_redis_connection
from rest_framework.generics import ListCreateAPIView

class UserCrud(viewsets.ModelViewSet):
    '''Class To perform CRUD api operations on CustomUser Model'''

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # throttle_classes = [CustomThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'city']         
         


class POSTCrud(viewsets.ModelViewSet):
    '''Class To perform CRUD api operations on Posts Model'''
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    throttle_classes = [CustomThrottle]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['id', 'user']    
    search_fields = ['id', '$content']           



# Custom Api Views

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
                record = APIData.objects.get(api=custom_api, data__id = data_id)
                return Response(record.data, status = status.HTTP_200_OK)
            
            except APIData.DoesNotExist:
                return Response({"error": "Data not found for this ID"}, status=status.HTTP_404_NOT_FOUND)
        else:
            records = APIData.objects.filter(api=custom_api).order_by('created_at')
            return Response({"data": [r.data for r in records]}, status = status.HTTP_200_OK)

    def post(self, request, endpoint):
        try:
            custom_api = CustomApi.objects.get(endpoint=endpoint)
        except CustomApi.DoesNotExist:
            return Response({"error": "Endpoint not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            data = request.data          
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
        


# Mock Api Views

class MockView(ListCreateAPIView):
    serializer_class = MockSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return MockData.objects.filter(Q(api__public_access = True) | Q(api__user = self.request.user))
        return MockData.objects.filter(api__public_access = True)


class MockHandlerView(APIView):
    def get(self, request, mockapi):
        try:
            mock_api = Mock.objects.get(mock_endpoint = mockapi)
        except Mock.DoesNotExist:
            return Response({"error" : "End-point not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.GET():
            query_params_dict = request.GET.dict()
            # query_params_json = json.dumps(query_params_dict)
            try:
                mock_data = MockData.objects.get(api = mock_api, method = request.method, body = query_params_dict)
            except:
                return Response({"error" : "End-point not found"}, status=status.HTTP_404_NOT_FOUND)
            response = Response(mock_data.response_msg, status = mock_data.response_code)
            return response
        else:
            try:
                mock_data = MockData.objects.get(api = mock_api, method = request.method, body__isnull = True)
            except:
                return Response({"error" : "End-point not found"}, status=status.HTTP_404_NOT_FOUND)
            response = Response(mock_data.response_msg, status = mock_data.response_code)
            return response
        
    def post(self, request, mockapi):
        try:
            mock_api = Mock.objects.get(mock_endpoint = mockapi)
        except Mock.DoesNotExist:
            return Response({"error" : "End-point not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.data:
            try:
                mock_data = MockData.objects.get(api = mock_api, method = request.method, body = request.data)
            except:
                return Response({"error" : "End-point not found"}, status=status.HTTP_404_NOT_FOUND)
            
            response = Response(mock_data.response_msg, status = mock_data.response_code)
            return response
        else:
            try:
                mock_data = MockData.objects.get(api = mock_api, method = request.method, body__isnull = True)
            except:
                return Response({"error" : "End-point not found"}, status=status.HTTP_404_NOT_FOUND)
            response = Response(mock_data.response_msg, status = mock_data.response_code)
            return response

    # def put(self, request, mockapi):
    #     try:
    #         mock_api = Mock.objects.get(mock_endpoint = mockapi)
    #     except Mock.DoesNotExist:
    #         return Response({"error" : "End-point not found"}, status=status.HTTP_404_NOT_FOUND)

    # def patch(self, request, mockapi):
    #     try:
    #         mock_api = Mock.objects.get(mock_endpoint = mockapi)
    #     except Mock.DoesNotExist:
    #         return Response({"error" : "End-point not found"}, status=status.HTTP_404_NOT_FOUND)

    # def delete(self, request, mockapi):
    #     try:
    #         mock_api = Mock.objects.get(mock_endpoint = mockapi)
    #     except Mock.DoesNotExist:
    #         return Response({"error" : "End-point not found"}, status=status.HTTP_404_NOT_FOUND)

