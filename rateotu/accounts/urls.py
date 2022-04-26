from django.conf.urls import url

from rest_framework_simplejwt import views as jwt_views
from djoser.urls.base import urlpatterns as djoser_urlpatterns

from rateotu.accounts import views


app_name = "accounts"
urlpatterns = [
    url(
        "auth/jwt/create/",
        views.CustomJwtTokenObtainPairView.as_view(),
        name="custom-jwt-create",
    ),
    url("auth/jwt/refresh/", jwt_views.TokenRefreshView.as_view(), name="jwt-refresh"),
    url("auth/jwt/verify/", jwt_views.TokenVerifyView.as_view(), name="jwt-verify"),
]

urlpatterns += djoser_urlpatterns
