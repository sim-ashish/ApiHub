from django.contrib import admin
from .models import *

@admin.register(Subscription)
class AdminCustomUser(admin.ModelAdmin):
    list_display = ['user']

@admin.register(CustomUser)
class AdminCustomUser(admin.ModelAdmin):
    list_display = ['name', 'email']

@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['user', 'content']

@admin.register(FoodCategory)
class AdminFoodCategory(admin.ModelAdmin):
    list_display = ['category']

@admin.register(FoodItem)
class AdminFoodItem(admin.ModelAdmin):
    list_display = ['food_name', 'category']

@admin.register(FoodOrders)
class AdminFoodOrders(admin.ModelAdmin):
    list_display = ['user', 'food_item']

@admin.register(FashionCategory)
class AdminFashionCategory(admin.ModelAdmin):
    list_display = ['category']

@admin.register(ClothMaterial)
class AdminClothMaterial(admin.ModelAdmin):
    list_display = ['material_name']

@admin.register(Cloth)
class AdminCloth(admin.ModelAdmin):
    list_display = ['cloth_name', 'cloth_category', 'cloth_material']


@admin.register(CustomApi)
class AdminCustomApi(admin.ModelAdmin):
    list_display = ['name', 'endpoint']


@admin.register(HitLog)
class AdminHitLog(admin.ModelAdmin):
    list_display = ['api', 'timestamp']


@admin.register(APIData)
class AdminAPIData(admin.ModelAdmin):
    list_display = ['id', 'api']

