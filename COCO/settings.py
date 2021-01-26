"""
Django settings for COCO project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.db.backends.postgresql.base import DatabaseWrapper
from django.db.backends.postgresql.operations import DatabaseOperations

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9+5u#n8q)x$+8iju=g(nlmd58yc6j2t-91%mt#1v%1ea712&w('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    # Self apps
    'Apps.ManageUsers.apps.UsersConfig',
    'Apps.ManageBarters.apps.BartersConfig',
    'Apps.ManageNotifications',
    'Apps.ManageSearches',
    'Apps.ManageReviews',
    'Apps.ManageChats',
    # Django apps
    'dj_rest_auth',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third Party apps
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'notify',
    'channels',
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

ROOT_URLCONF = 'COCO.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR) + '/Templates'],
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

WSGI_APPLICATION = 'COCO.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'coco_platform',
        'USER': 'cocoadmin',
        'PASSWORD': 'pZfMDy%sDpb07DXDVqs$JK@Ql#j6NY',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
LOGOUT_ON_PASSWORD_CHANGE = False
OLD_PASSWORD_FIELD_ENABLED = True
ASGI_APPLICATION = "COCO.asgi.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es-la'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(str(BASE_DIR), 'Files')
MEDIA_URL = '/coco-files/'
PASSWORD_RESET_TIMEOUT_DAYS = 1

# Mail interface
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "app.cocoplatform@gmail.com"  # Cambiar por correo del semillero
EMAIL_HOST_PASSWORD = "xaqtuyhjzxojouhj"  # Contraseña de aplicación
DOMAIN = "http://127.0.0.1:8000"

PIXABAY_API_KEY = '19499640-f691e6b92721afc93a5b52556'

SESSION_EXPIRE_AT_BROWSER_CLOSE = False


def lookup_cast(self, lookup_type, internal_type=None):
    if lookup_type in ('icontains', 'istartswith'):
        return "UPPER(unaccent(%s::text))"
    else:
        return super(DatabaseOperations, self).lookup_cast(lookup_type, internal_type)


def patch_unaccent():
    DatabaseOperations.lookup_cast = lookup_cast
    DatabaseWrapper.operators['icontains'] = 'LIKE UPPER(unaccent(%s))'
    DatabaseWrapper.operators['istartswith'] = 'LIKE UPPER(unaccent(%s))'


patch_unaccent()
