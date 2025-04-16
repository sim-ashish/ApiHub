from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('docs', views.docs, name='documentation'),
    path('custom-api', views.custom_docs, name='customApi'),
    path('mock',views.mock_view, name='mock'),
    path('profile', views.profile, name='profile'),
    path('register',views.User_register, name='register'),
    path('subscribe/<int:uID>', views.subscription_payment, name='subscribe'),
    path('login',views.User_login, name='login'),
    path('logout', views.User_logout, name='logout'),
]