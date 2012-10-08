"""
Based on http://code.google.com/p/modwsgi/wiki/IntegrationWithDjango
"""

import os, sys
import django.core.handlers.wsgi

os.environ['DJANGO_SETTINGS_MODULE'] = 'product_settings'

_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    if environ['wsgi.url_scheme'] == 'https':
        environ['HTTPS'] = 'on'

    return _application(environ, start_response)
