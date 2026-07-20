"""
Django settings for Student Feedback System.
"""

from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================================
# Security
# =====================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-CHANGE-THIS-KEY-BEFORE-DEPLOYMENT"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "127.0.0.1,localhost"
).split(",")


# =====================================================
# Applications
# =====================================================

INSTALLED_APPS = [
    # Django Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # Local Apps
    "accounts",
    "feedback",
    "faculty",
    "departments",
    "reports",
    "api",
]


# =====================================================
# Middleware
# =====================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "feedback_system.urls"


# =====================================================
# Templates
# =====================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
            ],
        },
    },
]


WSGI_APPLICATION = "feedback_system.wsgi.application"
ASGI_APPLICATION = "feedback_system.asgi.application"


# =====================================================
# Database
# =====================================================

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR/'db.sqlite3'}",
        conn_max_age=600,
    )
}


# =====================================================
# Password Validation
# =====================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# =====================================================
# Internationalization
# =====================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# =====================================================
# Static Files
# =====================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "feedback" / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)


# =====================================================
# Media Files
# =====================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =====================================================
# Authentication
# =====================================================

LOGIN_URL = "feedback:login"

LOGIN_REDIRECT_URL = "feedback:redirect_after_login"

LOGOUT_REDIRECT_URL = "feedback:login"


# =====================================================
# Session Security
# =====================================================

SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_HTTPONLY = False

SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# =====================================================
# Email
# =====================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get("himanshuranjan2213@gmail.com")

EMAIL_HOST_PASSWORD = os.environ.get("ryri fhcg iuob msci")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# =====================================================
# Production Security
# =====================================================

# if not DEBUG:

#     SESSION_COOKIE_SECURE = True

#     CSRF_COOKIE_SECURE = True

#     SECURE_SSL_REDIRECT = True

#     SECURE_PROXY_SSL_HEADER = (
#         "HTTP_X_FORWARDED_PROTO",
#         "https",
#     )
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# EMAIL_HOST_USER = "himanshuranjan2213@gmail.com"
# EMAIL_HOST_PASSWORD = "ryri fhcg iuob msci"

# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER