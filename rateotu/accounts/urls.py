from django.conf.urls import url

from rest_framework_simplejwt import views as jwt_views
from djoser.urls.base import urlpatterns as djoser_urlpatterns

from rateotu.accounts import views


# NOTE: Same AUTH service but different URLS
# NOTE: Permission protecting any of these URLs makes no sense (contradiction).
# JWTs are stateless, when refreshing a token, a user will be of AnonymousUser class,
# therefore endpoint will return 403.
# Since JWTs are managed at the clint level, each application must implement storage,
# expiry, renewal of JWTs, and RBAC. — This is a significant, security-sensitive
# responsibility.
# NOTE: All routes on client are 'role' protected.
# READ: https://www.django-rest-framework.org/api-guide/permissions/

app_name = "accounts"

customer_urlpatterns = [
    url(
        "auth/jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="ce-jwt-create",
    ),
    url(
        "auth/jwt/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="ce-refresh",
    ),
    url(
        "auth/jwt/verify/",
        jwt_views.TokenVerifyView.as_view(),
        name="ce-verify",
    ),
]

employee_urlspatterns = [
    url(
        "auth/jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="emp-jwt-create",
    ),
    url(
        "auth/jwt/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="emp-jwt-refresh",
    ),
    url(
        "auth/jwt/verify/",
        jwt_views.TokenVerifyView.as_view(),
        name="emp-jwt-verify",
    ),
]

customer_urlpatterns += djoser_urlpatterns
employee_urlspatterns += djoser_urlpatterns
