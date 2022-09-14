from .settings import *
import os


DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'searing_ai',
        'USER': 'postgres',
        'PASSWORD': '*****',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


USE_HTTPS_IN_ABSOLUTE_URLS = True  # make Stripe Checkout, email invitations, etc. use HTTPS instead of HTTP

ALLOWED_HOSTS = [
    'localhost:8000',
]


# Your email config goes here.
# see https://github.com/anymail/django-anymail for more details / examples

EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

ANYMAIL = {
    "MAILGUN_API_KEY": "key-****",
    "MAILGUN_SENDER_DOMAIN": 'localhost:8000',
}

SERVER_EMAIL = 'noreply@localhost:8000'
DEFAULT_FROM_EMAIL = 'ghb8745@gmail.com'
ADMINS = [('Your Name', 'ghb8745@gmail.com'),]

GOOGLE_ANALYTICS_ID = ''  # replace with your google analytics ID to connect to Google Analytics


STRIPE_LIVE_PUBLIC_KEY = os.environ.get("STRIPE_LIVE_PUBLIC_KEY", "<your publishable key>")
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "<your secret key>")
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY", "<your publishable key>")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "<your secret key>")
STRIPE_LIVE_MODE = True  # Change to True in production

# Mailchimp setup

# set these values if you want to subscribe people to a mailchimp list after they sign up.
MAILCHIMP_API_KEY = ''
MAILCHIMP_LIST_ID = ''
