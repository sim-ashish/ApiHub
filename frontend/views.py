from django.shortcuts import render, redirect
from .models import *
from api.models import Subscription
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from ApiHub.celery import Showmsg
from ApiHub.mail_send import mail


def index(request):
    host = request.get_host()
    return render(request, 'frontend/index.html')

def docs(request):
    endpoints = EndPoint.objects.all().order_by('id')
    return render(request, 'frontend/docs.html', {"endpoints" : endpoints})

def custom_docs(request):
    return render(request, 'frontend/customapi.html')


@login_required
def profile(request):
    return render(request, 'frontend/profile.html')


def User_register(request):
    if request.method == 'GET':
        form = UserRegisterForm()
        return render(request , 'frontend/register.html',{'form':form})
    else:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'frontend/register.html', {'form':form})


def User_login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request , 'frontend/login.html',{'form':form})
    else:
        form = AuthenticationForm(request = request, data = request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = uname, password = password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse('User Not Exist')
        else:
            return render(request, 'frontend/login.html', {'form':form})

@login_required
def User_logout(request):
    logout(request)
    return redirect('/')

def subscription_payment(request, uID):
    if request.method == 'GET':
        user = User.objects.get(id = uID)
        return render(request, 'frontend/subscription.html', locals())
    else:
        userId = request.POST.get('user-id')
        print("Userid : ", userId)
        user = User.objects.get(id = userId)
        Subscription.objects.create(user = user)
        return render(request, 'frontend/sub-done.html')
        