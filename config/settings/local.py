from .base import *
from .base import env


# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INTERNAL_IPS = ["127.0.0.1"]
# noqa
# APPS
# ------------------------------------------------------------------------------
INSTALLED_APPS += [
    "django_extensions",
    "debug_toolbar",
]
# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    "default": env.db("DATABASE_URL"),
}
# REST FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [
    "rest_framework_simplejwt.authentication.JWTAuthentication",
    "rest_framework.authentication.SessionAuthentication",
]
# AUTHENTICATION & AUTHORIZATION
# ------------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
DOMAIN = "localhost:3000"
