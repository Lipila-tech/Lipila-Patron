"""
Django settings for backend project.

Based on by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import environ
import sys
env = environ.Env()
# read .env
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')


# SET third party API Credentials
MTN_TARGET_ENV=env("MTN_TARGET_ENV")
MTN_COLLECTIONS_KEY=env("MTN_COLLECTIONS_KEY")
MTN_DISBURSEMENT_KEY=env("MTN_DISBURSEMENT_KEY")
MTN_PROVIDER_CALLBACK_HOST=env("MTN_PROVIDER_CALLBACK_HOST")
GOOGLE_OAUTH_CLIENT_ID=env("GOOGLE_OAUTH_CLIENT_ID")
BRAINTREE_MERCHANT_ID=env("BRAINTREE_MERCHANT_ID")
BRAINTREE_PUBLIC_KEY=env("BRAINTREE_PUBLIC_KEY")
BRAINTREE_PRIVATE_KEY=env("BRAINTREE_PRIVATE_KEY")

LOGIN_URI_TESTING = 'http://localhost:8000/accounts/auth-receiver/'
LOGIN_URI_PRODUCTION = 'https://lipila.pythonanywhere.com/accounts/auth-receiver/'

if env('ENV') == 'dev':
    LOGIN_URI = LOGIN_URI_TESTING
else:
    LOGIN_URI = LOGIN_URI_PRODUCTION

ALLOWED_HOSTS = ['lipila.pythonanywhere.com', 'localhost', '192.168.0.190']

# Application references
# https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    # 3rd Party apps
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
    'crispy_forms',
    'crispy_bootstrap4',
    'django_pagination_bootstrap',
    'bootstrap_modal_forms',
    'widget_tweaks',
    # My apps
    'api',
    'patron',
    'lipila',
    'accounts',
    'file_manager',

    # Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_pagination_bootstrap.middleware.PaginationMiddleware',
]

ROOT_URLCONF = 'backend.urls'

AUTHENTICATION_BACKENDS = [
    'accounts.auth_backends.EmailBackend',
    'accounts.auth_backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Custom context processor
                'accounts.context_processors.login_uri',
                'accounts.context_processors.data_client_id',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if env('DB_BACKEND') == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env('PSQL_NAME'),
            'USER': env('PSQL_USER'),
            'PASSWORD': env('PSQL_PASSWORD'),
            'HOST': env('PSQL_HOST'),
            'PORT': env('PSQL_PORT'),
            'TEST': {'NAME': 'testdatabse'},
        }
    }
elif env('DB_BACKEND') == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('SQL_NAME'),
            'USER': env('SQL_USER'),
            'PASSWORD':  env('SQL_PASSWORD'),
            'HOST': env('SQL_HOST'),
            'PORT': env('SQL_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
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

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

AUTH_USER_MODEL = 'accounts.CustomUser'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Specifies localhost port 3000 where the React
# server will be running is safe to receive requests
# from
CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000']

# Bootstrap
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Rest Framework config. Add all of this.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ),
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

STATICFILES_STORAGE = (
    'django.contrib.staticfiles.storage.StaticFilesStorage'
    if TESTING
    else 'whitenoise.storage.CompressedManifestStaticFilesStorage'
)

STATIC_ROOT = os.path.join(BASE_DIR, 'productionfiles')
STATICFILESDIRS = os.path.join(BASE_DIR, 'file_manager')
STATIC_URL = "static/"

LOGIN_REDIRECT_URL = "patron:profile"
LOGOUT_REDIRECT_URL = "accounts:signin"


if env('ENV') == 'dev':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = env('EMAIL_BACKEND')
    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_PORT = env('EMAIL_PORT')
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env('EMAIL_ID')
    EMAIL_HOST_PASSWORD = env('EMAIL_PW')

    DEFAULT_FROM_EMAIL = 'noreply<no_reply@domain.com>'


# set timezone
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lusaka'

USE_I18N = True

USE_L10N = True

USE_TZ = False