from django.contrib import admin
from travel_request.apps.request.models import Request, RequestMailConfig

class RequestAdmin(admin.ModelAdmin):
    list_display = ('requestor',
                    'manager',
                    'departure',
                    'destination',
                    'start_date',
                    'end_date',
                    'working_days',
                    'status')
    list_display_links = ('requestor',)
    readonly_fields = ('md5',)

admin.site.register(Request, RequestAdmin)

admin.site.register(RequestMailConfig)
