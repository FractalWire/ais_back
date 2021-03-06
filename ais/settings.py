"""
Django settings for ais project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import sys
import os
import csv

import yaml

import logging
from logformat import StyleAdapter


def environ_or_default(env_name: str, default: str) -> str:
    """Get environment variable or return a default value"""
    return os.environ[env_name] if env_name in os.environ else default


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ_or_default(
    'DJANGO_SECRET',
    's)$47740z$%$kg1&5=rg1z=nec%f-5adh^n%31b#nlmjf5^^@@')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # Must be False for no memory leak

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'aisreceiver.apps.AisreceiverConfig',
    'core.apps.CoreConfig',
    # 'geoserver.apps.GeoserverConfig',
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

ROOT_URLCONF = 'ais.urls'

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

WSGI_APPLICATION = 'ais.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ais',
        'USER': environ_or_default('POSTGRES_USER', 'postgres'),
        'PASSWORD': environ_or_default('POSTGRES_PASSWORD', 'postgres'),
        'HOST': environ_or_default('POSTGRES_HOST', '127.0.0.1'),
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# Configure logging
with open("logconfig.yml") as f:
    LOGGING = yaml.load(f, Loader=yaml.FullLoader)

logger = StyleAdapter(logging.getLogger(__name__))

# Disable logging for test
if len(sys.argv) > 1 and sys.argv[1] == 'test':
    logging.disable(logging.CRITICAL)


# TODO: Maybe not in settings ?
def handle_unhandled_exception(type_, value, traceback):
    """Called when an unhandled exception happened"""
    logger.critical("Unhandled exception", exc_info=(type_, value, traceback))


sys.excepthook = handle_unhandled_exception

# Configure csv dialect
DIALECT_NAME = 'postgres'
csv.register_dialect(DIALECT_NAME, delimiter='|', escapechar='\\',
                     lineterminator='\n', quoting=csv.QUOTE_NONE,
                     quotechar='', strict=True)
