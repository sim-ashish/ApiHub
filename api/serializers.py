from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
from django.contrib.auth.models import User
import re

class CustomUserSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'mobile', 'city', 'password', 'created_by']
        extra_kwargs = {
            'created_by': {'required': True},
        }
    
    def create(self, validated_data):
        user = validated_data.pop('created_by') 
        custom_user = CustomUser.objects.create(created_by=user, **validated_data)
        return custom_user

    def validate_password(self, value):
        if not re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", value):
            raise serializers.ValidationError("Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character")
        
        return value
    
    
    def validate_mobile(self, value):
        if not re.match("^[6-9]\d{9}$", value):
            raise serializers.ValidationError("Indian Numbers are Allowed")
        
        return value


class PostModelSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image', 'created_by']
        extra_kwargs = {
                    'created_by': {'required': True},
                }
        
    def create(self, validated_data):
        user = validated_data.pop('created_by')
        post = Post.objects.create(created_by=user, **validated_data)
        return post


class FoodCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ['id', 'category']


class FoodItemsSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    class Meta:
        model = FoodItem
        fields = ['id', 'category', 'food_name', 'food_price', 'created_by']
        extra_kwargs = {
                    'created_by': {'required': True},
                }

    def create(self, validated_data):
        user = validated_data.pop('created_by')
        food_item = FoodItem.objects.create(created_by=user, **validated_data)
        return food_item
    
class FoodOrderSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    class Meta:
        fields = ['id', 'user', 'food_item', 'total_price', 'order_time', 'created_by']
        extra_kwargs = {
                    'created_by': {'required': True},
                }
    
    def create(self, validated_data):
        user = validated_data.pop('created_by')
        food_order = FoodOrders.objects.create(created_by=user, **validated_data)
        return food_order


class FashionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FashionCategory
        fields = ['id', 'category']


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothMaterial
        fields = ['id', 'material_name']


class ClothSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    class Meta:
        model = Cloth
        fields = ['id', 'cloth_category', 'cloth_material', 'cloth_name', 'price', 'created_by']
        extra_kwargs = {
                    'created_by': {'required': True},
                }
    
    def create(self, validated_data):
        user = validated_data.pop('created_by')
        cloth = Cloth.objects.create(created_by=user, **validated_data)
        return cloth



class CustomApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomApi
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        cloth = CustomApi.objects.create(user=user, **validated_data)
        return cloth


class HitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HitLog
        fields = '__all__'


class APIDataSerializer(serializers.Serializer):
    data = serializers.JSONField()



class MockSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128, source='api.name')
    mock_endpoint = serializers.SlugField(source='api.mock_endpoint')
    public_access = serializers.BooleanField(source='api.public_access', write_only = True)
    method = serializers.ChoiceField(choices=MockData._meta.get_field('method').choices)
    body = serializers.JSONField(required=False)
    response_header = serializers.JSONField(required=False)
    response_msg = serializers.JSONField()
    response_code = serializers.ChoiceField(choices=MockData._meta.get_field('response_code').choices)

    class Meta:
        model = MockData
        fields = ['name', 'mock_endpoint','public_access', 'method', 'body', 'response_header', 'response_msg', 'response_code']


    def create(self, validated_data):
        print(validated_data)
        print("JWT : ",self.context['request'].user)
        api_data = validated_data.pop('api')  # Extract api fields (name, mock_endpoint)
        user = self.context['request'].user  # Assuming you have access to request context

        try:
            mock_obj, created = Mock.objects.get_or_create(
                user=user,
                name=api_data['name'],
                mock_endpoint=api_data['mock_endpoint'],
                public_access = api_data['public_access']
            )
        except:
            raise ValidationError("Endpoint Already Exist")
        
        body = validated_data.get('body')
        method = validated_data.get('method')
        if MockData.objects.filter(api=mock_obj, body=body, method=method).exists():
            raise ValidationError("An object with this combination of endpoint, body, and method already exists.")

        mock_data = MockData.objects.create(api=mock_obj, **validated_data)
        return mock_data
    