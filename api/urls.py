from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

############ JWT ##################
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
##################################################################################

User_router = DefaultRouter()
User_router.register('user', views.UserCrud, basename='user')

Post_router = DefaultRouter()
Post_router.register('post', views.POSTCrud, basename='post')


Custom_router = DefaultRouter()
Custom_router.register(r'custom-api', views.CustomAPIViewSet, basename='customapi')



urlpatterns = [
    path('',include(User_router.urls)),
    path('',include(Post_router.urls)),
    path('',include(Custom_router.urls)),
    path('endpoint/<slug:endpoint>/', views.DynamicApiHandler.as_view()),
    path('endpoint/<slug:endpoint>/<int:data_id>/', views.DynamicApiHandler.as_view()),
    path('gettoken/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/',TokenRefreshView.as_view(), name='token_refresh'),
]