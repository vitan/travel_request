from django import forms

class RequestForm(forms.Form):
    requestor_email = forms.EmailField(
        label='requestor email',
    )
    manager_email = forms.EmailField(
        label='manager_email',
    )
    departure = forms.CharField(
        label='departure',
        max_length=255,
    )
    destination = forms.CharField(
        label='destination',
        max_length=255,
    )
    start_date = forms.DateField(
        label='start date',
        widget=forms.DateInput({'class': 'datepicker1', })
    )
    end_date = forms.DateField(
        label='end date',
        widget=forms.DateInput({'class': 'datepicker2', })
    )
    working_days = forms.IntegerField(
        label='total number of working days',
    )
    reason = forms.CharField(
        label='bussiness reason for travel',
        widget=forms.Textarea,
    )
