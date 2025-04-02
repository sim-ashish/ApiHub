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