from django import forms
from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'location', 'category', 'urgency', 'status']

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget = forms.Select(choices=Request.CATEGORY_CHOICES)
        self.fields['urgency'].widget = forms.Select(choices=Request.URGENCY_LEVELS)
        self.fields['status'].widget = forms.Select(choices=Request.STATUS_CHOICES)
        

