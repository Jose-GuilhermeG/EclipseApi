from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views

from users import views

user_list = views.UserViewSet.as_view({"get": "list"})

user_control = views.UserViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

router = SimpleRouter()

router.register(
    "me/shopping-car", views.UserShppingCarViewSet, basename="user-shopping-car"
)

router.register("me/purchaseds", views.UserPurchasedViewset, basename="user-purchased")

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="user-register"),
    path("user/list", user_list, name="user-list"),
    path("me/", user_control, name="user-control"),
    path(
        "me/change-password/",
        views.ChangePasswordView.as_view(),
        name="user-change-password",
    ),
    path(
        "me/purchaseds/<id>/confirm-delivered/",
        views.confirm_delivered,
        name="user-purchased-confirm-delivered",
    ),
]

urlpatterns += router.urls

# auth urls
urlpatterns += [
    path("login/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", jwt_views.TokenVerifyView.as_view(), name="token_verify"),
]
