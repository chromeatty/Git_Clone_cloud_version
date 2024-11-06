from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Offer

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'description', 'location', 'category', 'status', 'quantity', 'availability_start', 'availability_end']

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget = forms.Select(choices=Offer.CATEGORY_CHOICES)
        self.fields['status'].widget = forms.Select(choices=Offer.STATUS_CHOICES)
        self.fields['availability_start'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        self.fields['availability_end'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')

    def clean_availability_start(self):
        availability_start = self.cleaned_data.get('availability_start')
        if availability_start < timezone.now():
            raise ValidationError("The start date and time must be in the future.")
        return availability_start

    def clean_availability_end(self):
        availability_start = self.cleaned_data.get('availability_start')
        availability_end = self.cleaned_data.get('availability_end')
        if availability_end is not None and availability_start is not None:
            if availability_end < availability_start:
                raise ValidationError("The end date and time cannot be before the start date and time.")
        return availability_end