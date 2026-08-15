from datetime import timedelta
from pathlib import Path

import environ

# ------------------------------------------------------------------------------
# Paths & Environment
# ------------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
  DEBUG=(bool, False),
)

environ.Env.read_env(BASE_DIR / ".env")

# ------------------------------------------------------------------------------
# Core Settings
# ------------------------------------------------------------------------------

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# ------------------------------------------------------------------------------
# Applications
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
  # Django apps
  "django.contrib.admin",
  "django.contrib.auth",
  "django.contrib.contenttypes",
  "django.contrib.sessions",
  "django.contrib.messages",
  "django.contrib.staticfiles",
  # Third-party apps
  "rest_framework",
  "django_filters",
  "corsheaders",
  "drf_spectacular",
  "rest_framework_simplejwt.token_blacklist",
  # Local apps
  "apps.accounts",
  "apps.organizations",
  "apps.core",
  "apps.candidates",
  "apps.engagement",
]

# ------------------------------------------------------------------------------
# Custom User
# ------------------------------------------------------------------------------

AUTH_USER_MODEL = "accounts.User"

# ------------------------------------------------------------------------------
# Middleware
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

# ------------------------------------------------------------------------------
# URLs / Templates
# ------------------------------------------------------------------------------

ROOT_URLCONF = "config.urls"

TEMPLATES = [
  {
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {
      "context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
      ],
    },
  },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------

DATABASES = {
  "default": env.db(
    "DATABASE_URL",
    default=(
      f"postgres://{env('DB_USER', default='postgres')}:"
      f"{env('DB_PASSWORD', default='')}@"
      f"{env('DB_HOST', default='localhost')}:"
      f"{env('DB_PORT', default='5432')}/"
      f"{env('DB_NAME', default='ong_back')}"
    ),
  ),
}

# ------------------------------------------------------------------------------
# Password Validation
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
  {
    "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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

# ------------------------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# ------------------------------------------------------------------------------
# Static & Media Files
# ------------------------------------------------------------------------------

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------------------------------------------------
# Default Primary Key
# ------------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------------------
# Django REST Framework
# ------------------------------------------------------------------------------

REST_FRAMEWORK = {
  "DEFAULT_PERMISSION_CLASSES": [
    "rest_framework.permissions.IsAuthenticated",
  ],
  "DEFAULT_AUTHENTICATION_CLASSES": [
    "rest_framework_simplejwt.authentication.JWTAuthentication",
  ],
  "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
  "PAGE_SIZE": 20,
  "DEFAULT_FILTER_BACKENDS": [
    "django_filters.rest_framework.DjangoFilterBackend",
    "rest_framework.filters.SearchFilter",
    "rest_framework.filters.OrderingFilter",
  ],
  "DEFAULT_THROTTLE_CLASSES": [
    "rest_framework.throttling.AnonRateThrottle",
    "rest_framework.throttling.UserRateThrottle",
  ],
  "DEFAULT_THROTTLE_RATES": {
    "anon": "100/hour",
    "user": "1000/hour",
    "login": "10/minute",
    "register": "5/hour",
  },
  "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
  "EXCEPTION_HANDLER": "config.exceptions.handler.custom_exception_handler",
}

# ------------------------------------------------------------------------------
# Simple JWT
# ------------------------------------------------------------------------------

SIMPLE_JWT = {
  "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
  "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
  "ROTATE_REFRESH_TOKENS": True,
  "BLACKLIST_AFTER_ROTATION": True,
}

# ------------------------------------------------------------------------------
# OpenAPI / Swagger
# ------------------------------------------------------------------------------

SPECTACULAR_SETTINGS = {
  "TITLE": "ONG Back API",
  "DESCRIPTION": "REST API for the engagement platform.",
  "VERSION": "1.0.0",
  "SERVE_INCLUDE_SCHEMA": False,
}

# ------------------------------------------------------------------------------
# CORS
# ------------------------------------------------------------------------------

# Development (override in local.py if preferred)
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=DEBUG)
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
