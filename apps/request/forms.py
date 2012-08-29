from django import forms

class RequestForm(forms.Form):
    requestor_email = forms.EmailField()
    manager_email = forms.EmailField()
    departure = forms.ChoiceField()
    destination = forms.ChoiceField()
    start_date = forms.DateField()
    end_date = forms.DateField()
    working_days = forms.IntegerField()
    reason = forms.CharField(
        widget=forms.Textarea,
    )
