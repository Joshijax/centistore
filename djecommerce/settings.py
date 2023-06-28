"""
Django settings for djecommerce project.

Generated by 'django-admin startproject' using Django 2.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jm@grao=k5j(av@a%5f#ar&a*5juffs*cnwt91b(6g94gs*ky2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', "54.236.22.165" "centiacollection.herokuapp.com",
                 "centiastore.com", "www.centiastore.com", "https://www.centiastore.com/"]


# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'django_countries',

    'core',
    "dashboard",
    'colorfield',
    "mathfilters",
    "storages",
    'corsheaders',

]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = [
    'https://www.centiastore.com',
    'http://www.centiastore.com',
    'https://centiastore.com',
    'http://centiastore.com',
    "http://127.0.0.1:7000",
    "http://127.0.0.1:8000"
]

CSRF_TRUSTED_ORIGINS = [
    'https://www.centiastore.com',
    'http://www.centiastore.com',
    'https://centiastore.com',
    'http://centiastore.com',
    "http://127.0.0.1:7000",
    "http://127.0.0.1:8000"
]

ROOT_URLCONF = 'djecommerce.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'djecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'u889468821_centistore',
#         'USER': 'u889468821_centistore',
#         'PASSWORD': 'Centcent12345',
#         'HOST': 'sql288.main-hosting.eu',
#         'PORT': '3306',
#         'OPTIONS': {
#             'init_command': "SET sql_mode = 'STRICT_TRANS_TABLES'"
#         }
#     }
# }


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]
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


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "core/static"),
    os.path.join(BASE_DIR, "dashboard/static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Auth

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

# CRISPY FORMS

CRISPY_TEMPLATE_PACK = 'bootstrap4'

ACCOUNT_EMAIL_VERIFICATION = "none"

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

FLUTTER_LIVE_PUBLIC_KEY = "FLWPUBK-c292d0073bee8868df08438b5aaaa1d8-X"
FLUTTER_LIVE_SECRET_KEY = "FLWSECK-26f1a16e64e736e239bfb7276978895b-188fcb1d169vt-X"

# encrption 26f1a16e64e7679f5274192a

FLUTTER_TEST_PUBLIC_KEY = "FLWPUBK_TEST-4710e2e530666ce562449e85a94c6963-X"
FLUTTER_TEST_SECRET_KEY = "FLWSECK_TEST-4890474339f09c345ed0492a590c4428-X"


# if not DEBUG:
#     DEFAULT_FILE_STORAGE = 'storages.backends.sftpstorage.SFTPStorage'
#     STATICFILES_STORAGE = 'storages.backends.sftpstorage.SFTPStorage'
#     SFTP_STORAGE_HOST = 'ftp://81.16.28.142'
#     SFTP_STORAGE_ROOT = '/home/u889468821/domains/centiastore.com/public_html'
#     SFTP_STORAGE_PARAMS = {
#         'username': 'u889468821.centiastore.com',
#         'password': 'Philanig1',
#     }
#     MEDIA_URL = 'http://centiastore.com/media/'
#     MEDIA_ROOT = ''
#     # MEDIA_ROOT = os.path.join(SFTP_STORAGE_ROOT, 'media')


# if not DEBUG:
#     DEFAULT_FILE_STORAGE = 'storages.backends.sftpstorage.SFTPStorage'
#     STATICFILES_STORAGE = 'storages.backends.sftpstorage.SFTPStorage'
#     SFTP_STORAGE_HOST = 'ftp://81.16.28.142'
#     SFTP_STORAGE_ROOT = '/home/u889468821/domains/centiastore.com/public_html'
#     SFTP_STORAGE_PARAMS = {
#         'username': 'u889468821.centiastore.com',
#         'password': 'Philanig1',
#     }
#     MEDIA_URL = 'http://centiastore.com/media/'
#     MEDIA_ROOT = ''
#     # MEDIA_ROOT = os.path.join(SFTP_STORAGE_ROOT, 'media')


USE_S3 = True
if USE_S3:
    AWS_ACCESS_KEY_ID = 'AKIASSUP5B7AHECXQ5OK'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_STORAGE_BUCKET_NAME = 'centistore'
    # AWS_LOCATION = 'static'
    AWS_S3_SECURE_URLS = True
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # STATIC_LOCATION = 'static'
    # STATICFILES_STORAGE = 'web.storage_backends.StaticStorage'

    # AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    # STATICFILES_DIRS = [
    #     os.path.join(BASE_DIR, 'static'),
    # ]

    # STATIC_ROOT = os.path.join(BASE_DIR, 'http://%s.s3.amazonaws.com//static/'  % AWS_STORAGE_BUCKET_NAME)
    # STATIC_URL='https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    # ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
    # STATICFILES_FINDERS = (           'django.contrib.staticfiles.finders.FileSystemFinder',    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # )

    # S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    # PUBLIC_MEDIA_LOCATION = 'media'
    # MEDIA_URL = f'{S3_URL}/{PUBLIC_MEDIA_LOCATION}/'
    # MEDIA_ROOT = 'https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
    # DEFAULT_FILE_STORAGE = 'djecommerce.storage_backends.PublicMediaStorage'
