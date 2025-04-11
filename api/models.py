from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_subscriber = models.BooleanField(default=False)


# Users
class CustomUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.BigIntegerField()
    city = models.CharField(max_length=100)
    password = models.CharField(max_length=300)


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='posts/')


# Food Models
class FoodCategory(models.Model):
    category = models.CharField(max_length=100)

class FoodItem(models.Model):
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='fooditem')
    food_name = models.CharField(max_length=200)
    food_price = models.DecimalField(max_digits=10, decimal_places=2)

class FoodOrders(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='foodorder')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_time = models.DateTimeField(auto_now_add=True)


# Ecommerce Models

class FashionCategory(models.Model):
    category = models.CharField(max_length=100)

class ClothMaterial(models.Model):
    material_name = models.CharField(max_length=100)

class Cloth(models.Model):
    cloth_category = models.ForeignKey(FashionCategory, on_delete=models.CASCADE, related_name='clothes')
    cloth_material = models.ForeignKey(ClothMaterial, on_delete=models.SET_NULL, null=True, related_name='clothmaterial')
    cloth_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2) 




################################################# Custom Api #################################################

class CustomApi(models.Model):
    auto_id = models.BigIntegerField(default = 1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    endpoint = models.SlugField(unique=True)
    success_response = models.JSONField()
    error_response = models.JSONField()
    validations = models.JSONField(default=dict, blank=True)
    public = models.BooleanField(default=True)


    def __str__(self):
        return str(self.endpoint)

'''
{
"name" : "Age Checker",
"endpoint" : "agecheck",
"success_response" : {"message" : "Valid age!"},
"error_response" : {"message" : "Invalid age!"},
"validations":{
        "age" : {"type" : "int", "min" : 18, "max" : 65},
        "name" : {"type" : "str"}
    },
"public" : true
}
'''


class HitLog(models.Model):
    api = models.ForeignKey(CustomApi, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    request_data = models.JSONField(null=True, blank=True)
    returned_status = models.IntegerField()

    # def __str__(self):
    #     return self.api


class APIData(models.Model):
    api = models.ForeignKey(CustomApi, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.api




############################################# Mock Api############################################
class MockApi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mockapi = models.SlugField(unique=True)
    header = models.JSONField(default = dict, null=True)
    response_msg = models.JSONField(null=True)
    response_code = models.IntegerField(null=True)


    def __str__(self):
        return f'MOCK : {self.mockapi}'
    
class QueryMockData(models.Model):
    mock = models.ForeignKey(MockApi, on_delete=models.CASCADE)
    query_params = models.JSONField(default=dict,null=True)
    header = models.JSONField(default = dict, null=True)
    response_msg = models.JSONField(null=True)
    response_code = models.IntegerField(null=True)
