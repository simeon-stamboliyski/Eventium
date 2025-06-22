from django import forms
from .models import Event
from django.utils import timezone

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['slogan', 'location', 'start_time', 'available_tickets', 'key_features', 'banner_url']
        widgets = {
            'slogan': forms.TextInput(attrs={'placeholder': 'Provide an appealing text...'}),
            'key_features': forms.Textarea(attrs={'placeholder': 'Provide important event details...'}),
            'banner_url': forms.URLInput(attrs={'placeholder': 'An optional banner image URL...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].initial = timezone.now()