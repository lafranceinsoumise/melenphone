"""
Django settings for melenchonPB project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys
from django.core.exceptions import ImproperlyConfigured
import dj_database_url


def env_to_bool(variable, default):
    value = os.environ.get(variable)
    if value is None: return default
    if value.lower() in ['true', 't', 'yes', 'y']:
        return True
    if value.lower() in ['false', 'f', 'no', 'n']:
        return False
    return default


def env_required(variable):
    try:
        return os.environ[variable]
    except KeyError:
        raise ImproperlyConfigured('Required environment variable: %s' % (variable,))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

DEBUG = env_to_bool('DEBUG', False)

# Security parameters

SECRET_KEY = env_required('SECRET_KEY')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(' ')

SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = env_to_bool('COOKIE_SECURE', True)

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# the cookie should be available from js --> set to False
CSRF_COOKIE_HTTPONLY = False

# allow displaying website only from same origin
X_FRAME_OPTIONS = 'SAMEORIGIN'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

if DEBUG == False:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG' if DEBUG else 'INFO',
                'class': 'logging.StreamHandler',
                'stream': sys.stderr
            }
        },
        'loggers': {
            'django': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': True,
            },
        }
    }

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'callcenter',
    'rest_framework',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'melenchonPB.urls'

WSGI_APPLICATION = 'melenchonPB.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config('DATABASE_URL', default='sqlite:///db.sqlite3', conn_max_age=600)
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Auth user model
#

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    'accounts.backend.JLMOAuth2'
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

ANGULAR_URL = '/ng'
ANGULAR_ROOT = os.path.join(BASE_DIR, '../frontend/dist/')

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'static'))
STATICFILES_DIRS = (
    ANGULAR_ROOT,
)

# redis
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_UNIX_SOCKET = os.environ.get('REDIS_UNIX_SOCKET')
REDIS_MAX_CONNECTIONS = 4

# channels

CHANNEL_BACKEND = os.environ.get('CHANNEL_BACKEND', 'inmemory')

if CHANNEL_BACKEND == 'inmemory':
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": 'asgiref.inmemory.ChannelLayer',
            "ROUTING": "callcenter.routing.channel_routing",
        },
    }
elif CHANNEL_BACKEND == 'redis':
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "asgi_redis.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(REDIS_HOST, REDIS_PORT)],
            },
            "ROUTING": "callcenter.routing.channel_routing",
        },
    }
else:
    raise ImproperlyConfigured('Unknown CHANNEL_BACKEND type : "%s"' % (CHANNEL_BACKEND,))

# In settings.py

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
}

# callhub parameters
CALLHUB_API_KEY = env_required('CALLHUB_API_KEY')
CALLHUB_WEBHOOK_TOKEN = os.environ.get('CALLHUB_WEBHOOK_TOKEN', 'note')

# jlm-auth parameters
AUTHORIZATION_URL = env_required('AUTHORIZATION_URL')
ACCESS_TOKEN_URL = env_required('ACCESS_TOKEN_URL')
DEFAULT_SCOPE = ['view_profile']
SCOPE_SEPARATOR = ' '
PROFILE_URL = env_required('PROFILE_URL')

# where to redirect once logged in
LOGIN_REDIRECT = '/ng/oauth_redirect'

# the base uri to use to access this server from the outside world
# used for oauth2 and callhub webhooks
REDIRECT_BASE = os.environ.get('REDIRECT_BASE')

# OAuth client parameters
CLIENT_ID = env_required('CLIENT_ID')
CLIENT_SECRET = env_required('CLIENT_SECRET')

# minimum lenght of call so that it is counted, in seconds
MIN_DELAY = 30

# parameters for calculating phi earnings
from decimal import Decimal

BASE_PHI = 10
MULTIPLIER_RESET = 3600
PHI_FIRST_CALL = 50
PHI_ALEA = 2
MULTIPLIER_GROWTH = Decimal('0.1')
MAX_MULTIPLIER = 3