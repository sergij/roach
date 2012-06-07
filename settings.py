# -*- coding: utf-8 -*-

import os
import sys

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
ENV_ROOT = os.path.dirname(PROJECT_ROOT)

# пути к приложениям
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sergij Kozlov', 'sergijkozlov@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'data.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'
SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), 'static')
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'

# Additional locations of static files
STATICFILES_DIRS = (
    ('main', os.path.join(PROJECT_ROOT, 'static')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
#    'compressor.finders.CompressorFinder',
)
# Make this unique, and don't share it with anybody.
SECRET_KEY = ')a^ce1qg8hda#@-09@4qxt6lmbz8wctg2^eqa_t0cjhdi3y&n&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'grappelli',
    'filebrowser',

    'south',
    'registration',
    'social_auth',
    'sorl.thumbnail',
    # 'pytils',
    # 'widget_tweaks',
    # 'compressor',
    'storages',
    'account',
    'main',
)

from local_settings import *