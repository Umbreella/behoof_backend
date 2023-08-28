import os
import sys
from datetime import timedelta
from pathlib import Path

from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent

config = {
    **dotenv_values('.env'),
    **dotenv_values('.env.local'),
    **dotenv_values('.env.development.local'),
    **dotenv_values('.env.production.local'),
    **os.environ,
}

if 'test' in sys.argv:
    config = {
        **dotenv_values('.env.test.local')
    }

SECRET_KEY = config.get('DJANGO_APP_SECRET_KEY')

DEBUG = int(config.get('DJANGO_APP_DEBUG', 0))

ALLOWED_HOSTS = config.get('DJANGO_APP_ALLOWED_HOSTS').split(' ')

PASSWORD_HASHERS = config.get('DJANGO_APP_PASSWORD_HASHERS').split(' ')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'django_filters',
    'drf_yasg',
    'graphene_django',
    'graphene_gis',
    'leaflet',
    'phonenumber_field',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework_simplejwt.token_blacklist',

    'foods',
    'restaurants',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'behoof.urls'

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

WSGI_APPLICATION = 'behoof.wsgi.application'

DATABASES = {
    'default': {},
    'master': {
        'ENGINE': config.get('DJANGO_APP_DATABASE_SQL_ENGINE'),
        'NAME': config.get('DJANGO_APP_DATABASE_SQL_MASTER_DATABASE'),
        'USER': config.get('DJANGO_APP_DATABASE_SQL_MASTER_USER'),
        'PASSWORD': config.get('DJANGO_APP_DATABASE_SQL_MASTER_PASSWORD'),
        'HOST': config.get('DJANGO_APP_DATABASE_SQL_MASTER_HOST'),
        'PORT': config.get('DJANGO_APP_DATABASE_SQL_MASTER_PORT'),
        'TEST': {
            'DEPENDENCIES': [],
        },
        'ATOMIC_REQUESTS': True,
    },
    'slave': {
        'ENGINE': config.get('DJANGO_APP_DATABASE_SQL_ENGINE'),
        'NAME': config.get('DJANGO_APP_DATABASE_SQL_REPLICA_DATABASE'),
        'USER': config.get('DJANGO_APP_DATABASE_SQL_REPLICA_USER'),
        'PASSWORD': config.get('DJANGO_APP_DATABASE_SQL_REPLICA_PASSWORD'),
        'HOST': config.get('DJANGO_APP_DATABASE_SQL_REPLICA_HOST'),
        'PORT': config.get('DJANGO_APP_DATABASE_SQL_REPLICA_PORT'),
        'TEST': {
            'DEPENDENCIES': ['master', ],
            'MIRROR': 'master',
        },
    },
}

DATABASE_ROUTERS = config.get('DJANGO_APP_DATABASE_ROUTER', '').split(' ')

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'users.backends.AuthBackend.AuthBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.NumericPasswordValidator'
        ),
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PHONENUMBER_DEFAULT_REGION = 'RU'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = config.get('DJANGO_APP_CSRF_TRUSTED_ORIGINS').split(' ')
CORS_ALLOWED_ORIGINS = config.get('DJANGO_APP_CORS_ALLOWED_ORIGINS').split(' ')

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'access-control-allow-credentials',
    'access-control-expose-headers',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'stripe-signature',
]

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

GRAPHENE = {
    'SCHEMA': 'behoof.graphql.schema.schema',
}
