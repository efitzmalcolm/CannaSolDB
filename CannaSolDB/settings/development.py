from .base import *

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'CannaSolDev',
        'USER': 'dev',
        'PASSWORD': 'dev',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
