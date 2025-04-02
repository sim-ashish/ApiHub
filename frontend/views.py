from django.shortcuts import render
from .models import *

# Create your views here.


def index(request):
    host = request.get_host()
    print("Host : ", host)
    return render(request, 'frontend/index.html')

def docs(request):
    endpoints = EndPoint.objects.all()
    return render(request, 'frontend/docs.html', {"endpoints" : endpoints})