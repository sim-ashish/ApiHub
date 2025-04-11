from django.urls import path, include
from api.views import (
            CustomAPIViewSet, 
            DynamicApiHandler, 
            MockView, 
            POSTCrud, 
            UserCrud
        )
from rest_framework.routers import DefaultRouter

############ JWT ##################
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
##################################################################################

User_router = DefaultRouter()
User_router.register('user', UserCrud, basename='user')

Post_router = DefaultRouter()
Post_router.register('post', POSTCrud, basename='post')


Custom_router = DefaultRouter()
Custom_router.register(r'custom-api', CustomAPIViewSet, basename='customapi')



urlpatterns = [
    path('',include(User_router.urls)),
    path('',include(Post_router.urls)),
    path('',include(Custom_router.urls)),
    path('mock/', MockView.as_view(), name='mock-create'),
    path('endpoint/<slug:endpoint>/', DynamicApiHandler.as_view()),
    path('endpoint/<slug:endpoint>/<int:data_id>/', DynamicApiHandler.as_view()),
    path('gettoken/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/',TokenRefreshView.as_view(), name='token_refresh'),
]