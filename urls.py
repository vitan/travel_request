from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from apps.request.views import travel_request, feedback

urlpatterns = patterns('',
    # Examples:
    url(r'^$', redirect_to, {'url': 'travel_request/'}),
    url(r'^travel_request/$', travel_request, name='travel_request'),
    url(r'^travel_request/feedback/(\d{1})/([a-z\d]{32})/$', feedback, name='feedback'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
