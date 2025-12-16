"""
Django settings for Canteen_Manager project.
(Cleaned & Fixed for Local Windows PC)
"""

from pathlib import Path
import os

# 1. Base Directory (Pathlib ka use karke)
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Security Settings
SECRET_KEY = '---w7!kw@w^@0y1exh7i3hjm%tnu!vt18c2+938k9+(((f(g-9'

# LOCAL KE LIYE YE SAB FALSE RAKHEIN
DEBUG = True
ALLOWED_HOSTS = ["*"]

# HTTPS Security (Local computer par ye False hona chahiye)
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# 3. Application Definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'management',
    'django.contrib.humanize',
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

# Aapke folder ka naam 'Canteen_Manager' hai (Capital Letters)
ROOT_URLCONF = 'Canteen_Manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Agar templates folder hai to
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Canteen_Manager.wsgi.application'

# 4. Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata' # India Time Zone kar diya hai
USE_I18N = True
USE_TZ = True

# 5. Static & Media Files (Sabse Important Fix)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Windows par backslash (\) ki jagah Path join use karna safe hai
STATICFILES_DIRS = [
    BASE_DIR / 'management' / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 6. Login Redirects
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home_dashboard'
LOGOUT_REDIRECT_URL = 'login'