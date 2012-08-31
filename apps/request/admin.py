from django.contrib import admin
from travel_request.apps.request.models import Request, MailConfig

class RequestAdmin(admin.ModelAdmin):
    list_display = ('requestor_email',
                    'manager_email',
                    'departure',
                    'destination',
                    'start_date',
                    'end_date',
                    'working_days',
                    'status',
                    'update_date'
                   )
    readonly_fields = ('md5',)

admin.site.register(Request, RequestAdmin)

class MailConfigAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'email',
                    'is_cc')

admin.site.register(MailConfig, MailConfigAdmin)
