from django.contrib import admin
from travel_request.apps.request.models import Request, MailConfig
from travel_request.apps.request.views import ACTION
from django.core.mail import EmailMultiAlternatives
from datetime import datetime

class RequestAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.status is not 0:
            obj.update_date = datetime.now()
            obj.save()

            subject = "Request Feedback Change"
            feedback  ="%s at %s <font style='color:red'>%s</font> the following request"\
                    %(obj.manager_email,
                      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      ACTION[str(obj.status)])

            email_body = feedback+"<br><br>\
                    From: %s<br>\
                    Start: %s To: %s<br>\
                    Working off days: %s<br>\
                    Reason: %s<br><br>"\
                    %(obj.requestor_email,
                      obj.start_date,
                      obj.end_date,
                      obj.working_days,
                      obj.reason)

            #FIXME the manager should be only one? so tos is to
            tos = [entry.email for entry in MailConfig.objects.filter(is_cc=False)]
            ccs = [entry.email for entry in MailConfig.objects.filter(is_cc=True)]
            tos.append(obj.requestor_email)

            msg = EmailMultiAlternatives(subject=subject,
                                         from_email="hosted-no-reply@redhat.com",
                                         to=tos,
                                         cc=ccs,
                                         headers={'Cc': ','.join(ccs)})
            
            msg.attach_alternative(email_body, "text/html")
            msg.send(fail_silently=False)
        else:
            pass

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
    search_fields  = ['requestor_email',
                      'manager_email',
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

class MailConfigAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'email',
                    'is_cc')

admin.site.register(MailConfig, MailConfigAdmin)
