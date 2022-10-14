"""
Django settings for Searing.ai project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from dotenv import load_dotenv

import os
from pathlib import Path
import lockdown
import sentry_sdk
import boto3

from sentry_sdk.integrations.django import DjangoIntegration
from django.utils.translation import gettext_lazy

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

LOCKDOWN_PASSWORDS = os.environ.get('LOCKDOWN_PASSWORDS')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# sentry
sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']
# timezone
USE_TZ = True

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.forms',
]

# Put your third-party apps here
THIRD_PARTY_APPS = [
    'allauth',  # allauth account/registration management
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'drf_spectacular',
    'rest_framework_api_key',
    'celery_progress',
    'storages',
    'widget_tweaks',
    'annoying',
    'guardian',
]

PEGASUS_APPS = [
    'pegasus.apps.examples.apps.PegasusExamplesConfig',
    'pegasus.apps.employees.apps.PegasusEmployeesConfig',
]

# Put your project-specific apps here
PROJECT_APPS = [
    'apps.users.apps.UserConfig',
    'apps.api.apps.APIConfig',
    'apps.web',
    'apps.data',
    'lockdown'  # remove before beta
]

LAST_APP = ['django_cleanup.apps.CleanupConfig']

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PEGASUS_APPS + PROJECT_APPS + LAST_APP


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.web.locale_middleware.UserLocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'lockdown.middleware.LockdownMiddleware',  # remove before beta
]

ROOT_URLCONF = 'searing_ai.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.web.context_processors.project_meta',
                # this line can be removed if not using google analytics
                 'apps.web.context_processors.google_analytics_id',
            ],
        },
    },
]

WSGI_APPLICATION = 'searing_ai.wsgi.application'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DJANGO_DATABASE_NAME', 'searing_ai'),
        'USER': os.environ.get('DJANGO_DATABASE_USER', 'postgres'),
        'PASSWORD': os.environ.get('DJANGO_DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DJANGO_DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DJANGO_DATABASE_PORT', '5432'),
    }
}



# Auth / login stuff

# Django recommends overriding the user model even if you don't think you need to because it makes
# future changes much easier.
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_REDIRECT_URL = '/'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Allauth setup

ACCOUNT_ADAPTER = 'apps.users.adapter.EmailAsUsernameAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True



# User signup configuration: change to "mandatory" to require users to confirm email before signing in.
# or "optional" to send confirmation emails but not require them
ACCOUNT_EMAIL_VERIFICATION = 'optional'

GUARDIAN_MONKEY_PATCH = False

AUTHENTICATION_BACKENDS = (
    # Needed to log in by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
    'guardian.backends.ObjectPermissionBackend',
)


# enable social login
SOCIALACCOUNT_PROVIDERS = { 
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }, 
}


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGE_COOKIE_NAME = 'searing_ai_language'
LANGUAGES = [
    ('en', gettext_lazy('English')),
    ('fr', gettext_lazy('French')),
]
LOCALE_PATHS = (
    BASE_DIR / 'locale',
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# TODO: remove CORS headers on digitalocean after using CDN
# TODO: implement compression
# note: fetching static and media files will be slow for now
# until implementing a CDN

USE_SPACES = True

if USE_SPACES:

    session = boto3.Session(
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'static_root'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    # public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    DEFAULT_FILE_STORAGE = 'apps.data.storage_backends.PublicMediaStorage'
    # private media settings
    PRIVATE_MEDIA_LOCATION = 'private'
    PRIVATE_FILE_STORAGE = 'apps.data.storage_backends.PrivateMediaStorage'


else:
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'static_root'
    MEDIA_ROOT = BASE_DIR / 'media'
    MEDIA_URL = '/media/'

STATICFILES_DIRS = [BASE_DIR / 'static']


# uncomment to use manifest storage to bust cache when file change
# note: this may break some image references in sass files which is why it is not enabled by default
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# TODO: ensure that any user cannot view all usernames by connecting to media server


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# future versions of Django will use BigAutoField as the default, but it can result in unwanted library
# migration files being generated, so we stick with AutoField for now.
# change this to BigAutoField if you're sure you want to use it and aren't worried about migrations.
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Email setup
ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get('MAILGUN_API_KEY'),
    "MAILGUN_SENDER_DOMAIN": 'searing.ai'
}

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
# use in production
# see https://github.com/anymail/django-anymail for more details/examples
# EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

# Django sites

SITE_ID = 1

# DRF config
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'apps.api.permissions.IsAuthenticatedOrHasUserAPIKey',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Searing.ai',
    'DESCRIPTION': 'Learn shit. Real fast.',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
    "SWAGGER_UI_SETTINGS": {
        "displayOperationId": True,
    },
    "PREPROCESSING_HOOKS": [
        "apps.api.schema.filter_schema_apis",
    ],
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization"
            }
        }
    },
    "SECURITY": [{"ApiKeyAuth": [], }],
}

# Celery setup (using redis)
CELERY_BROKER_URL = os.environ.get('REDIS_URL')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')

# Pegasus config

# replace any values below with specifics for your project
PROJECT_METADATA = {
    'NAME': gettext_lazy('Searing.ai'),
    'URL': 'https://searing.ai',
    'DESCRIPTION': gettext_lazy("Learn shit. Real fast."),
    'IMAGE': 'https://upload.wikimedia.org/wikipedia/commons/2/20/PEO-pegasus_black.svg',
    'KEYWORDS': 'AI, Education, Learning, University, Professor, St',
    'CONTACT_EMAIL': 'darinkishore@protonmail.com',
}

USE_HTTPS_IN_ABSOLUTE_URLS = False  # set this to True in production to have URLs generated with https instead of http

SERVER_EMAIL = 'noreply@searing.ai'
DEFAULT_FROM_EMAIL = 'darin@searing.ai'
ADMINS = [('Darin Kishore', 'darin@searing.ai'),]
# Add your google analytics ID to the environment or default value to connect to Google Analytics
GOOGLE_ANALYTICS_ID = ''


# Stripe config

# modeled to be the same as https://github.com/dj-stripe/dj-stripe
STRIPE_LIVE_PUBLIC_KEY = os.environ.get("STRIPE_LIVE_PUBLIC_KEY", "<your publishable key>")
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "<your secret key>")
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY", "pk_test_<your publishable key>")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "sk_test_<your secret key>")
STRIPE_LIVE_MODE = False  # Change to True in production




LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} "{name}" {message}',
            'style': '{',
            'datefmt': '%d/%b/%Y %H:%M:%S'  # match Django server time format
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'searing_ai': {
            'handlers': ['console'],
            'level': os.environ.get('SEARING_AI_LOG_LEVEL', 'INFO'),
        }
    }
}
