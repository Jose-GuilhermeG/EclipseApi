from django.urls import path , include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from users import views

user_list = views.UserViewSet.as_view(
    {'get': 'list'}
)

user_control = views.UserViewSet.as_view(
    {
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }
)

urlpatterns = [
    path(
        'register/',
        views.RegisterView.as_view(),
        name='user-register'    
    ),
    path(
        'user/list',
        user_list,
        name='user-list'
    ),
    path(
        'me/',
        user_control,
        name='user-control'
    ),
    path(
        'me/change-password/',
        views.ChangePasswordView.as_view(),
        name='user-change-password'
    ),
    path(
        'me/shopping-car/',
        views.UserShopingCarItensListView.as_view(),
        name="user-shopping-car"
    )
    
]

#auth urls
urlpatterns += [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
]