from pathlib import Path
import os
from decouple import config
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = False #True for development
ALLOWED_HOSTS = ['localhost','www.localhost','hospitals.localhost','patients.localhost','pharmacy.localhost','doctors.localhost','dev.localhost','prescribemate.com','www.prescribemate.com','hospitals.prescribemate.com','patients.prescribemate.com','pharmacy.prescribemate.com','doctors.prescribemate.com','dev.prescribemate.com',]

BASE_DOMAIN = config('BASE_DOMAIN')

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
PARENT_HOST = 'localhost:8000' if DEBUG else 'prescribemate.com'

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

MESSAGE_TAGS = {
    messages.DEBUG: 'message-info',
    messages.INFO: 'message-info',
    messages.SUCCESS: 'message-success',
    messages.WARNING: 'message-warning',
    messages.ERROR: 'message-error',
}

WSGI_APPLICATION = 'prescribemate.wsgi.application'

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

LOGIN_URL = '/login/'
AUTH_USER_MODEL = 'common.User'
AUTH_PASSWORD_VALIDATORS = []
AUTHENTICATION_BACKENDS = ['common.auth_backend.UsernameBackend']

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

USE_SUBDOMAIN_ROUTING = True
CSRF_TRUSTED_ORIGINS = [
    'http://dev.localhost:8000',
    'http://doctors.localhost:8000',
    'http://hospitals.localhost:8000',
    'http://patients.localhost:8000',
    'http://pharmacy.localhost:8000',
    'http://www.localhost:8000',
    'http://dev.localhost:8000',
    'http://localhost:8000',
    'https://dev.prescribemate.com',
    'https://doctors.prescribemate.com',
    'https://hospitals.prescribemate.com',
    'https://patients.prescribemate.com',
    'https://pharmacy.prescribemate.com',
    'https://www.prescribemate.com',
    'https://prescribemate.com',
]
SESSION_COOKIE_DOMAIN = '.prescribemate.com' #'.localhost' or BASE_DOMAIN........ None for development 
CSRF_COOKIE_DOMAIN = '.prescribemate.com' #'.localhost' or BASE_DOMAIN....... None for development
#these next four lines goes comment in development
CSRF_COOKIE_SECURE = True  # Set True in production (HTTPS only)
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # Send session cookie only over HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JS access to session cookie

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mx5.alpha.net.bd'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'info@nutsutechnologies.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'info@nutsutechnologies.com'
SERVER_EMAIL = 'info@nutsutechnologies.com'