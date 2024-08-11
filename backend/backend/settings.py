import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = (
    'django-insecure-508yx%04(-1rh@o74nuath+i4adict$)@p7k3=(^!xflgsta1_' # спрятать в .env
)

DEBUG = True
# True если использует SQLite, иначе используется PostgreSQL.
SQLAITE = True
# При запуске проекта через manage.py runserver - значение True.
LOCALLY = True
# True если используется защищённый протокол передачи данных в интернете.
HTTPSecure = False

DOMAIN_NAME = '.env' if not DEBUG else (  # подтянуть из .env
    '127.0.0.1:8000' if LOCALLY else 'localhost'
)

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', DOMAIN_NAME]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'djoser',

    'api.apps.ApiConfig',
    'recipes.apps.RecipesConfig',
    'users.apps.UsersConfig',
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

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

if SQLAITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'sqlite/db.sqlite3'
            if LOCALLY else '/sqlite/db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'django'),
            'USER': os.getenv('POSTGRES_USER', 'django'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', ''),
            'PORT': os.getenv('DB_PORT', 5432),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Astrakhan'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/django_static/'
STATIC_ROOT = BASE_DIR / 'collected_static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' if LOCALLY else '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PAGINATION_CLASS': (
        'api.v1.paginations.FootgramPageNumberPagination'
    ),
}

AUTH_USER_MODEL = 'users.UserFoodgram'

DJOSER = {
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'current_user': 'api.v1.serializers.UserFoodgramSerializer',
        'user': 'api.v1.serializers.UserFoodgramSerializer',
        'user_create': 'api.v1.serializers.UserCreateFoodgramSerializer',
    },
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.AllowAny'],
        'user_list': ['rest_framework.permissions.AllowAny'],
    },
}

INVALID_USER_NAMES = ('me', 'Me', 'eM', 'ME')
PATTERN_USERNAME = r'^[\w.@+-]+\Z'

SEARCH_PARAM = 'name'

PAGE_SIZE = 6
PAGE_SIZE_QUERY_PARAM = 'limit'

EXTRA_TABULAR_INLINE = 1
RECIPES_LIMIT = 1

MIN_COOKING_TIME = 1
MIN_AMOUNT = 1
LENGTH_USERNAME = 150
LENGTH_TEXT_SMALL = 32
LENGTH_TEXT_SHORT = 64
LENGTH_TEXT_MEDIUM = 128
LENGTH_TEXT_LONG = 256

STRING_CHARACTERS = ('abcdefghijklmnopqrstuvwxyz'
                     'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                     '1234567890')
LENGTH_SHORT_LINK = 4

HTTPS = 's' if HTTPSecure else ''
