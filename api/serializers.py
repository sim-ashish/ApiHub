from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'mobile', 'city', 'password']

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


from rest_framework import serializers

class APIDataSerializer(serializers.Serializer):
    data = serializers.JSONField()
