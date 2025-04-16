from django.urls import path, include
from api.views import (
            CustomAPIViewSet, 
            DynamicApiHandler,
            MockHandlerView, 
            MockView, 
            POSTCrud, 
            UserCrud,
            FoodCategoryView,
            FoodItemView,
            FoodOrderView,
            FashionCategoryView,
            ClothMaterialView,
            ClothView,
        )
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

User_router = DefaultRouter()
User_router.register('user', UserCrud, basename='user')

Post_router = DefaultRouter()
Post_router.register('post', POSTCrud, basename='post')

Food_item_router = DefaultRouter()
Food_item_router.register('food-item', FoodItemView, basename='food-item')

Food_order_router = DefaultRouter()
Food_order_router.register('food-order', FoodOrderView, basename='food-order')

Cloths_router = DefaultRouter()
Cloths_router.register('clothes', ClothView, basename='clothes')

Custom_router = DefaultRouter()
Custom_router.register(r'custom-api', CustomAPIViewSet, basename='customapi')

urlpatterns = [
    path('',include(User_router.urls)),
    path('',include(Post_router.urls)),
    path('',include(Food_item_router.urls)),
    path('',include(Food_order_router.urls)),
    path('',include(Cloths_router.urls)),
    path('',include(Custom_router.urls)),
    path('food-category', FoodCategoryView.as_view(), name = 'food-category'),
    path('fashion-category', FashionCategoryView.as_view(), name = 'fashion-category'),
    path('cloth-material', ClothMaterialView.as_view(), name = 'cloth-material'),
    path('mock/', MockView.as_view(), name='mock-create'),
    path('mock/<slug:mockapi>/', MockHandlerView.as_view(), name='mock-handle'),
    path('endpoint/<slug:endpoint>/', DynamicApiHandler.as_view()),
    path('endpoint/<slug:endpoint>/<int:data_id>/', DynamicApiHandler.as_view()),
    path('gettoken/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/',TokenRefreshView.as_view(), name='token_refresh'),
]