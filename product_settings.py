# Django settings for authenticity project.
from settings import *

# Set DEBUG = False on production server.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

SEND_BROKEN_LINK_EMAILS = True

ADMINS = (
    ('WeiTao Zhou', 'weizhou@redhat.com'),
)

MANAGERS = ADMINS

ROOT_URLCONF = 'urls'

# If app is deployed under a proxied host, please set DEPLOY_PROXY_PATH accordingly.
# By changing DEPLOY_PROXY_PATH, FORCE_SCRIPT_NAME&HOSTNAME will be changed accordingly.
USE_PROXY = True
DEPLOY_PROXY_PATH = ""
if USE_PROXY:
    DEPLOY_PROXY_PATH = "/travel-request"
    # https://docs.djangoproject.com/en/dev/ref/settings/#use-x-forwarded-host
    # default is false, if it's deployed under proxy, must set it to True.
    USE_X_FORWARDED_HOST = True
    # This is used to add site-wide URL prefix.
    FORCE_SCRIPT_NAME = DEPLOY_PROXY_PATH

HOSTNAME = "http://" + socket.gethostname() + DEPLOY_PROXY_PATH + "/travel_request/"

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'dbname',                      # Or path to database file if using sqlite3.
#        'USER': 'user',                      # Not used with sqlite3.
#        'PASSWORD': 'password',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}

# SERVER_TYPE could be : Stage, Devel, Test, etc. Leave blank for production server.
SERVER_TYPE = ""

