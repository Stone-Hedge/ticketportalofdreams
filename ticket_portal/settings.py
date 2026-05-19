import os
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.auth.hashers import make_password

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-secret-key-change')
DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = [h.strip() for h in os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if h.strip()]
TIME_ZONE = os.getenv('TIME_ZONE', 'Europe/London')
USE_TZ = True

DATA_DIR = Path(os.getenv('DATA_DIR', BASE_DIR / 'data'))
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH = os.getenv('DATABASE_PATH', str(DATA_DIR / 'db.sqlite3'))

INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','portal'
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware','portal.middleware.PasscodeRateLimitMiddleware'
]
ROOT_URLCONF = 'ticket_portal.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates','DIRS': [BASE_DIR / 'templates'],'APP_DIRS': True,
    'OPTIONS': {'context_processors': ['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']},
}]
WSGI_APPLICATION = 'ticket_portal.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': DATABASE_PATH}}
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'en-gb'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

GENERAL_PASSCODE_HASH = os.getenv('GENERAL_PASSCODE_HASH') or make_password(os.getenv('GENERAL_PASSCODE', 'gooners'))
ADMIN_PASSCODE_HASH = os.getenv('ADMIN_PASSCODE_HASH') or make_password(os.getenv('ADMIN_PASSCODE', 'gooners-admin'))
LOGIN_URL = '/passcode/'
