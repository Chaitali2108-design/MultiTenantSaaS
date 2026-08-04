from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9+w6t1hgoe^a2*9fjf3esh2!hqi6qu@t1(q#xhcw-&a9(pfg7u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "axes",
    'accounts',
    "organizations.apps.OrganizationsConfig",
    'dashboard',
    'projects',

    'rest_framework',
    'system_settings',
    "audit.apps.AuditConfig",
    'api',
    'rest_framework_simplejwt.token_blacklist',
    "reports",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "audit.middleware.AuditMiddleware",
    "system_settings.middleware.MaintenanceModeMiddleware",
    "axes.middleware.AxesMiddleware",
    "accounts.middleware.TenantMiddleware",
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates',
            BASE_DIR / 'projects' / 'templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'projects.context_processors.reminders',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


AUTH_USER_MODEL = 'accounts.User'

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Session expires after 30 minutes
SESSION_COOKIE_AGE = 1800

SESSION_SAVE_EVERY_REQUEST = True

# Expire session when browser closes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Session security

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = False

SESSION_COOKIE_SAMESITE = "Lax"

# Security Headers

X_FRAME_OPTIONS = "DENY"

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"


# Production only
SECURE_SSL_REDIRECT = False

# Login Attempt Security

AXES_FAILURE_LIMIT = 5

AXES_COOLOFF_TIME = 1

AXES_RESET_ON_SUCCESS = True

AXES_LOCKOUT_PARAMETERS = [
    ["username", "ip_address"],
]


AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

REST_FRAMEWORK = {

    "DEFAULT_AUTHENTICATION_CLASSES": [

        "rest_framework_simplejwt.authentication.JWTAuthentication",

    ],


    "DEFAULT_PERMISSION_CLASSES": [

        "rest_framework.permissions.IsAuthenticated",

    ],


    "DEFAULT_THROTTLE_CLASSES": [

        "rest_framework.throttling.UserRateThrottle",

        "rest_framework.throttling.AnonRateThrottle",

    ],


    "DEFAULT_THROTTLE_RATES": {

        "user": "100/hour",

        "anon": "20/hour",

    },

    "EXCEPTION_HANDLER":
    "api.exceptions.custom_exception_handler",

}


from datetime import timedelta


SIMPLE_JWT = {

    # Access token used for API requests
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=15
    ),


    # Refresh token used to get new access token
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=7
    ),


    # Rotate refresh token after use
    "ROTATE_REFRESH_TOKENS": True,


    # Blacklist old refresh tokens
    "BLACKLIST_AFTER_ROTATION": True,


    # Authentication header
    "AUTH_HEADER_TYPES": (
        "Bearer",
    ),


    # User identifier
    "USER_ID_FIELD": "id",


    "USER_ID_CLAIM": "user_id",
}

# Security Headers

X_FRAME_OPTIONS = "DENY"


SECURE_CONTENT_TYPE_NOSNIFF = True


SECURE_REFERRER_POLICY = (
    "same-origin"
)


SECURE_BROWSER_XSS_FILTER = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = "chandelechaitali@gmail.com"

EMAIL_HOST_PASSWORD = "izvpfpkrkrehhzls"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER