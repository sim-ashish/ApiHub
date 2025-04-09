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
