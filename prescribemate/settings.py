from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG')
ALLOWED_HOSTS = ['*']

BASE_DOMAIN = config('BASE_DOMAIN', default='192.168.0.101')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'doctors',
    'patients',
    'hospitals',
    'pharmacy',
    'common',
]

INSTALLED_APPS += [
    'django_hosts',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware', # must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.SubdomainMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware', # must be last
]

ROOT_URLCONF = 'prescribemate.urls'
ROOT_HOSTCONF = 'prescribemate.hosts'
DEFAULT_HOST = 'www'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'prescribemate.wsgi.application'

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql',
		'NAME': config('DB_NAME'),
		'USER': config('DB_USER'),
		'PASSWORD': config('DB_PASSWORD'),
		'HOST': '127.0.0.1',
		'PORT': '6432',  # PgBouncer port
    }
}

AUTH_USER_MODEL = 'common.User'
AUTH_PASSWORD_VALIDATORS = []
AUTHENTICATION_BACKENDS = ['common.auth_backend.UsernameBackend']

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

USE_SUBDOMAIN_ROUTING = True
SESSION_COOKIE_DOMAIN = f".{BASE_DOMAIN}"
CSRF_COOKIE_DOMAIN = f".{BASE_DOMAIN}"