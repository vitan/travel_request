from django.contrib import admin
from travel_request.apps.request.models import Request, RequestMailConfig

class RequestAdmin(admin.ModelAdmin):
    list_display = ('requestor_id',
                    'manager_id',
                    'departure',
                    'destination',
                    'start_date',
                    'end_date',
                    'working_days',
                    'reason',
                   'status')
admin.site.register(Request)
admin.site.register(RequestMailConfig)
