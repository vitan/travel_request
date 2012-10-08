from django.contrib import admin
from apps.request.models import Request, Team, MailConfig

class RequestAdmin(admin.ModelAdmin):
    list_display = ('requestor_email',
                    'team',
                    'departure',
                    'destination',
                    'start_date',
                    'end_date',
                    'working_days',
                    'status',
                    'update_date'
                   )
    readonly_fields = ('md5',)
    search_fields  = ['requestor_email',
                      'team',
                      'departure',
                      'destination',
                      'working_days',]
    ordering = ['-update_date', 'start_date', 'status']
    list_filter = ('start_date',
                   'end_date',
                   'status',
                   'working_days',
                   'update_date',)

admin.site.register(Request, RequestAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'functional_manager_email')
    search_fields = ['name',
                     'functional_manager_email',]

admin.site.register(Team, TeamAdmin)

class MailConfigAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'email',
                    'is_cc')

admin.site.register(MailConfig, MailConfigAdmin)
