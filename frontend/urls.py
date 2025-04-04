from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('docs', views.docs, name='documentation'),
    path('profile', views.profile, name='profile'),
    path('register',views.User_register, name='register'),
    path('login',views.User_login, name='login'),
    path('logout', views.User_logout, name='logout'),
]