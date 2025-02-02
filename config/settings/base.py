"""
Base settings to build other settings files upon.
"""
import environ
from pathlib import Path
from datetime import timedelta

env = environ.Env()

# GENERAL
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
env.read_env(BASE_DIR / ".env")

PROJECT_NAME = "rateotu"

APPS_DIR = BASE_DIR / PROJECT_NAME

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")
# APPS
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    # django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "rest_framework",
    "djoser",
    "corsheaders",
    "django_filters",
    "channels",
    # Local
    "rateotu.accounts.apps.AccountsAppConfig",
    "rateotu.customers.apps.CustomersAppConfig",
    "rateotu.employees.apps.EmployeesAppConfig",
    "rateotu.menus.apps.MenusAppConfig",
    "rateotu.orders.apps.OrdersAppConfig",
    "rateotu.tables.apps.TablesAppConfig",
    "rateotu.notifications.apps.NotificationsAppConfig",
]
# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# DATABASES
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# PROJECT CONFIG
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(env("REDIS_HOST"), env("REDIS_PORT"))],
        },
    },
}

APPEND_SLASH = False
# REST FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}
# AUTHENTICATION & AUTHORIZATION
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"

DJOSER = {
    "ACTIVATION_URL": "accounts/activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "accounts/password/reset/confirm/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "TOKEN_MODEL": None,
}

SITE_NAME = env("SITE_NAME")

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    "USER_ID_FIELD": "username",
    "USER_ID_CLAIM": "username",
}
# PASSWORD VALIDATION
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# INTERNATIONALIZATION / LOCALIZATION
# ------------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True
# STATIC FILES (CSS, JAVASCRIPT, IMAGES)
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
SERVER_EMAIL = env("SERVER_EMAIL")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_HOST_USER = SERVER_EMAIL
DEFAULT_FROM_EMAIL = SERVER_EMAIL
# LOGGING
# ------------------------------------------------------------------------------
LOGS_DIR = BASE_DIR / "logs"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "simple": {
            "format": "[%(asctime)s %(levelname)s %(name)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S %z",
        },
        "verbose": {
            "format": "[%(asctime)s %(levelname)s %(name)s] [%(pathname)s:%(lineno)d] %(message)s",  # noqa
            "datefmt": "%Y-%m-%d %H:%M:%S %z",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "rateotu_logfile": {
            "level": "INFO",
            # 'filters': ['require_debug_true'],
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "rateotu.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "rateotu": {
            "handlers": ["rateotu_logfile"],
            "propagate": False,
            "level": "DEBUG",
        },
    },
}
