from django.db import models

# Create your models here.

class EndPoint(models.Model):
    endpoint_name = models.CharField(max_length=50)
    success_code = models.CharField(max_length=20)
    error_code = models.CharField(max_length=20)
    endpoint_description = models.TextField()
    endpoint_url = models.CharField(max_length=250)