from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'frontend/index.html')

def docs(request):
    return render(request, 'frontend/docs.html')