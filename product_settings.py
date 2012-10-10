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

HOSTNAME = "http://" + socket.gethostname() + "/travel-request/travel_request/"

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

