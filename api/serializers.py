from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
import re

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'mobile', 'city', 'password']

    def validate_password(self, value):
        if not re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", value):
            raise serializers.ValidationError("Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character")
        
        return value
    
    
    def validate_mobile(self, value):
        if not re.match("^[6-9]\d{9}$", value):
            raise serializers.ValidationError("Indian Numbers are Allowed")
        
        return value




class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image']



class CustomApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomApi
        fields = '__all__'


class HitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HitLog
        fields = '__all__'



class APIDataSerializer(serializers.Serializer):
    data = serializers.JSONField()



# class MockSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(max_length = 128, source='api.name')
#     mock_endpoint = serializers.SlugField(source='api.mock_endpoint')

#     class Meta:
#         model = MockData
#         fields = ['name','mock_endpoint','method','body','response_header','response_msg','response_code']

#     def create(self, **validate):
#         self.super().create()

class MockSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128, source='api.name')
    mock_endpoint = serializers.SlugField(source='api.mock_endpoint')
    method = serializers.ChoiceField(choices=MockData._meta.get_field('method').choices)
    body = serializers.JSONField(required=False)
    response_header = serializers.JSONField(required=False)
    response_msg = serializers.JSONField()
    response_code = serializers.ChoiceField(choices=MockData._meta.get_field('response_code').choices)

    class Meta:
        model = MockData
        fields = ['name', 'mock_endpoint', 'method', 'body', 'response_header', 'response_msg', 'response_code']


    def create(self, validated_data):
        print(validated_data)
        api_data = validated_data.pop('api')  # Extract api fields (name, mock_endpoint)
        user = self.context['request'].user  # Assuming you have access to request context

        try:
            mock_obj, created = Mock.objects.get_or_create(
                user=user,
                name=api_data['name'],
                mock_endpoint=api_data['mock_endpoint']
            )
        except:
            raise ValidationError("Endpoint Already Exist")
        body = validated_data.get('body')
        method = validated_data.get('method')
        if MockData.objects.filter(api=mock_obj, body=body, method=method).exists():
            raise ValidationError("An object with this combination of endpoint, body, and method already exists.")

        mock_data = MockData.objects.create(api=mock_obj, **validated_data)
        return mock_data
    

# class MockSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(max_length=128, source='api.name', read_only=True)
#     mock_endpoint = serializers.SlugField(source='api.mock_endpoint', read_only=True)
#     method = serializers.ChoiceField(choices=MockData._meta.get_field('method').choices)
#     body = serializers.JSONField(required=False)
#     response_header = serializers.JSONField(required=False)
#     response_msg = serializers.JSONField()
#     response_code = serializers.ChoiceField(choices=MockData._meta.get_field('response_code').choices)

#     # Add these fields separately to accept input
#     input_name = serializers.CharField(write_only=True)
#     input_mock_endpoint = serializers.SlugField(write_only=True)

#     class Meta:
#         model = MockData
#         fields = [
#             'input_name', 'input_mock_endpoint',
#             'name', 'mock_endpoint',
#             'method', 'body', 'response_header', 'response_msg', 'response_code'
#         ]

#     def create(self, validated_data):
#         input_name = validated_data.pop('input_name')
#         input_mock_endpoint = validated_data.pop('input_mock_endpoint')
#         user = self.context['request'].user

#         mock_obj, created = Mock.objects.get_or_create(
#             user=user,
#             name=input_name,
#             mock_endpoint=input_mock_endpoint
#         )

#         mock_data = MockData.objects.create(api=mock_obj, **validated_data)
#         return mock_data