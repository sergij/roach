import os

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
ENV_ROOT = os.path.dirname(PROJECT_ROOT)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 's
        'NAME': 'roach',
        'USER': 'roach',                      # Not used with sqlite3.
        'PASSWORD': 'rO@cH',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    },
}

COMPRESS_ENABLED = False
COMPRESS_YUI_BINARY = os.path.join(ENV_ROOT, 'bin', 'yuicompressor-2.4.7.jar')
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.yui.YUICSSFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.yui.YUIJSFilter']

AWS_ACCESS_KEY_ID = 'AKIAIKYGIWHOHZBRPUIAa'
AWS_SECRET_ACCESS_KEY = 'rKcSJpsp5wYf3rAoTLK+OgDpMI/3pZUfvqliJWBZa'
AWS_STORAGE_BUCKET_NAME = 'dev2lookwishstatic'
# AWS_LOCATION = 'static'
from S3 import CallingFormat
AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

#AWS_S3_SECURE_URLS = False
STORAGES_S3BOTO_MULTI = {
    'media': {
        'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID,
        'AWS_SECRET_ACCESS_KEY': 'rKcSJpsp5wYf3rAoTLK+OgDpMI/3pZUfvqliJWBZ',
        'AWS_STORAGE_BUCKET_NAME': 'dev2lookwishmedia',
        'AWS_LOCATION': 'media',
        'AWS_S3_CUSTOM_DOMAIN': 'cdn-dev2.lookwish.ru',
        'AWS_CALLING_FORMAT': AWS_CALLING_FORMAT,
        'AWS_S3_SECURE_URLS': False,
    },
    'static': {
        'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID,
        'AWS_SECRET_ACCESS_KEY': 'rKcSJpsp5wYf3rAoTLK+OgDpMI/3pZUfvqliJWBZ',
        'AWS_STORAGE_BUCKET_NAME': 'dev2lookwishstatic',
        'AWS_LOCATION': 'static',
        'AWS_S3_CUSTOM_DOMAIN': 'cdn-dev2.lookwish.ru',
        'AWS_CALLING_FORMAT': AWS_CALLING_FORMAT,
        'AWS_S3_SECURE_URLS': False,
   }
}
DEFAULT_FILE_STORAGE = 'storages.backends.s3botomulti.S3BotoStorage_media'
STATICFILES_STORAGE = 'storages.backends.s3botomulti.S3BotoStorage_static'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# COMPRESS_STORAGE = STATICFILES_STORAGE

