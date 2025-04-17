from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import *
from .models import *
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from api.throttling import CustomThrottle
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.core.cache import cache
from api.custom_field_validations import email_validation
import re
import json
from django_redis import get_redis_connection
from rest_framework.generics import ListCreateAPIView, ListAPIView
from api.custom_permissions import IsOwnerOrAdmin

class UserCrud(viewsets.ModelViewSet):
    '''This class will handle all CRUD operations related to Custom Users'''

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    throttle_classes = [CustomThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'city']  

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)       

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsAuthenticatedOrReadOnly(), IsOwnerOrAdmin()]
        # return [IsAuthenticated()]
         


class POSTCrud(viewsets.ModelViewSet):
    '''This class will handle all CRUD operations related to Posts'''

    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    throttle_classes = [CustomThrottle]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['id', 'user']    
    search_fields = ['id', '$content']           


class FoodCategoryView(ListAPIView):
    '''This class will List all food categories'''

    def get_queryset(self):
        return FoodCategory.objects.all()
    def get_serializer_class(self):
        return FoodCategoriesSerializer
    

class FoodItemView(viewsets.ModelViewSet):
    '''This class will handle all CRUD operations related to Food Items'''

    queryset = FoodItem.objects.all()
    serializer_class = FoodItemsSerializer
    throttle_classes = [CustomThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['food_name', 'category'] 
    search_fields = ['id', '$food_name', 'category'] 

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)       

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsAuthenticatedOrReadOnly(), IsOwnerOrAdmin()]
        # return [IsAuthenticated()]
    

class FoodOrderView(viewsets.ModelViewSet):
    '''This class will handle all CRUD operations related to Food Orders'''

    queryset = FoodOrders.objects.all()
    serializer_class = FoodOrderSerializer
    throttle_classes = [CustomThrottle]
    filter_backends = [DjangoFilterBackend]
    search_fields = ['id', 'user'] 

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)       

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsAuthenticatedOrReadOnly(), IsOwnerOrAdmin()]
        # return [IsAuthenticated()]
    

class FashionCategoryView(ListAPIView):
    '''This class will List all Fashion Categories'''

    throttle_classes = [CustomThrottle]
    def get_queryset(self):
        return FashionCategory.objects.all()
    def get_serializer_class(self):
        return FashionCategorySerializer
    

class ClothMaterialView(ListAPIView):
    '''This class will List all Cloth Materials'''

    throttle_classes = [CustomThrottle]
    def get_queryset(self):
        return ClothMaterial.objects.all()
    def get_serializer_class(self):
        return MaterialSerializer
    

class ClothView(viewsets.ModelViewSet):
    '''This class will handle all CRUD operations related to Cloth'''

    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer
    throttle_classes = [CustomThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cloth_name', 'cloth_category', 'cloth_material'] 
    search_fields = ['id', '$cloth_name', 'cloth_category', 'cloth_material'] 

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)       

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsAuthenticatedOrReadOnly(), IsOwnerOrAdmin()]
        # return [IsAuthenticated()]


# Custom Api Views

class CustomAPIViewSet(viewsets.ModelViewSet):
    '''Class To create and show Custom Api's with name , endpoint, status_codes and validations'''

    serializer_class = CustomApiSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomThrottle]

    def get_queryset(self):
        return CustomApi.objects.filter(user=self.request.user, public = True)

    
    def perform_create(self, serializer):                   
        serializer.save(user=self.request.user)



class DynamicApiHandler(APIView):
    '''This class will handle all the Create, List, Update and Delete for Custom Api's Data'''

    permission_classes = [IsAuthenticated] 

    def get(self, request: Request, endpoint: str, data_id: int = None) ->  Response :
        '''This fucntion handle the List and Retrieve the endpoint Data'''

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

    def post(self, request: Request, endpoint: str) -> Response :
        '''This function will handle post data for custom api's endpoint'''

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
                        if rules["regex"] == "email":
                            if not email_validation(value):
                                return Response({"error": f"{field} is not in the correct format"}, status=status.HTTP_400_BAD_REQUEST)
                        # if not re.match(rules["regex"], value):
                        #     return Response({"error": f"{field} is not in the correct format"}, status=status.HTTP_400_BAD_REQUEST)

                if rules.get("type") == "boolean":
                    if not isinstance(value, bool):
                        return Response({"error": f"{field} must be a Boolean"}, status=status.HTTP_400_BAD_REQUEST)

        # Getting id to uniquely identify data from redis or db, if validation success!!
        cache_key = f'key:{endpoint}'
        # api_id = cache.get(str(endpoint), None)
        api_id = cache.get(cache_key, None)

        if api_id is None:
            api_id = int(custom_api.auto_id)
            # cache.set(str(endpoint), api_id, timeout= 60 * 60 *24)      # storing for 24 hrs
            cache.set(cache_key, api_id, timeout= None)      # storing for 24 hrs


        # # Save data if valid
        data['id'] = api_id
        APIData.objects.create(api=custom_api, data=data)
        cache.set(str(endpoint), api_id + 1, timeout= None)            # Increasing the id for that specific endpoint
        return Response(custom_api.success_response, status=status.HTTP_201_CREATED)
    
    def put(self, request: Request , endpoint: str , data_id: int = None) -> Response : 
        try:
            custom_api = CustomApi.objects.get(endpoint=endpoint)
        except CustomApi.DoesNotExist:
            return Response({"error": "Endpoint not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if data_id:
            try:
                record = APIData.objects.get(api=custom_api, data__id = data_id)
            except APIData.DoesNotExist:
                return Response({"error": "Data not found for this ID"}, status=status.HTTP_404_NOT_FOUND)
            try:
                data = request.data          
            except Exception:
                return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
            


        else:
            return Response({"error": "Required an lookup id"}, status=status.HTTP_400_BAD_REQUEST)
        
  
    def patch(self, request: Request , endpoint: str , data_id:int = None) -> Response : 
        try:
            custom_api = CustomApi.objects.get(endpoint=endpoint)
        except CustomApi.DoesNotExist:
            return Response({"error": "Endpoint not found"}, status=status.HTTP_404_NOT_FOUND)
        if data_id:
            try:
                record = APIData.objects.get(api=custom_api, data__id = data_id)
            except APIData.DoesNotExist:
                return Response({"error": "Data not found for this ID"}, status=status.HTTP_404_NOT_FOUND)
            try:
                data = request.data          
            except Exception:
                return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
            

        else:
            return Response({"error": "Required an lookup id"}, status=status.HTTP_400_BAD_REQUEST)
          
    def delete(self, request: Request , endpoint: str , data_id: int = None) -> Response: 
        '''This function will handle delete request for custom api's endpoint'''

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
    '''This class will perform GET and POST operations for Mock Api's'''

    serializer_class = MockSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        print("View : ", self.request.user)
        serializer.save()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return MockData.objects.filter(Q(api__public_access = True) | Q(api__user = self.request.user))
        return MockData.objects.filter(api__public_access = True)


class MockHandlerView(APIView):
    '''Class To handle requests of Mock Api's'''

    def get(self, request: str , mockapi: str) -> Response :
        '''This function will serve get method'''

        try:
            mock_api = Mock.objects.get(mock_endpoint = mockapi)
        except Mock.DoesNotExist:
            return Response({"error" : "End-point not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.GET:
            print("Query Params",request.GET)
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
                mock_data = MockData.objects.get(api = mock_api, method = request.method, body = {})
            except:
                print("Else ka exept")
                return Response({"error" : "End-point not found"}, status=status.HTTP_404_NOT_FOUND)
            response = Response(mock_data.response_msg, status = mock_data.response_code)
            return response
        
    def post(self, request: Request , mockapi: str) -> Response:
        '''This function will server post method of mock api'''

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
                mock_data = MockData.objects.get(api = mock_api, method = request.method, body = {})
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
