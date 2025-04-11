from rest_framework import serializers
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
        # fields = '__all__'


    def create(self, validated_data):
        api_data = validated_data.pop('api')  # Extract api fields (name, mock_endpoint)
        user = self.context['request'].user  # Assuming you have access to request context

        mock_obj, created = Mock.objects.get_or_create(
            user=user,
            name=api_data['name'],
            mock_endpoint=api_data['mock_endpoint']
        )

        mock_data = MockData.objects.create(api=mock_obj, **validated_data)
        return mock_data
    

