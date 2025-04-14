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
class Mock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    mock_endpoint = models.SlugField(unique=True)


class MockData(models.Model):
    api = models.ForeignKey(Mock, on_delete=models.CASCADE)
    method = models.CharField(max_length=10, choices = [('GET', 'GET'),('POST','POST'),('PUT','PUT'),('PATCH', 'PATCH'),('DELETE', 'DELETE')])
    body = models.JSONField(default=dict, null=True)
    response_header = models.JSONField(null=True)
    response_msg = models.JSONField()
    response_code = models.IntegerField(choices = [(100, 100), (101, 101), (102, 102), (103, 103),(200, 200), (201, 201), (202, 202), (203, 203), (204, 204), (205, 205), (206, 206),(207, 207), (208, 208), (226, 226),(300, 300), (301, 301), (302, 302), (303, 303), (304, 304), (305, 305), (306, 306),(307, 307), (308, 308),(400, 400), (401, 401), (402, 402), (403, 403), (404, 404), (405, 405), (406, 406),(407, 407), (408, 408), (409, 409), (410, 410), (411, 411), (412, 412), (413, 413),(414, 414), (415, 415), (416, 416), (417, 417), (418, 418), (421, 421), (422, 422),(423, 423), (424, 424), (425, 425), (426, 426), (428, 428), (429, 429),(431, 431), (451, 451),(500, 500), (501, 501), (502, 502), (503, 503), (504, 504), (505, 505), (506, 506),(507, 507), (508, 508), (510, 510), (511, 511)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['api', 'method','body'], name='unique_user_post')
        ]



# Monitoring

class Request_logs(models.Model):
    req_user = models.CharField(max_length=15)
    req_method = models.CharField(max_length=10)
    endpoint = models.CharField(max_length=256)
    ip_address = models.CharField(max_length=20)
    request_time = models.DateTimeField(auto_now_add=True)
