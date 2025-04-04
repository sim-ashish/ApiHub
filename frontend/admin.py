from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(EndPoint)
class AdminEndPoint(admin.ModelAdmin):
    list_display = ['id','endpoint_name']