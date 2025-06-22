from django import forms
from django.contrib.auth.models import User
from .models import Organizer

class OrganizerForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = ['company_name', 'phone_number', 'secret_key']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'placeholder': 'Enter a company name...',
                'aria-describedby': 'id_company_name_helptext',
                'id': 'id_company_name',
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Enter a valid phone number (digits only)...',
                'id': 'id_phone_number',
            }),
            'secret_key': forms.PasswordInput(attrs={
                'placeholder': 'Enter a secret key like <1234>...',
                'aria-describedby': 'id_secret_key_helptext',
                'maxlength': '4',
                'id': 'id_secret_key',
            }),
        }
        labels = {
            'company_name': 'Company Name:',
            'phone_number': 'Phone Number:',
            'secret_key': 'Secret Key:',
        }
        help_texts = {
            'company_name': '*Allowed names contain letters, digits, spaces, and hyphens.',
            'secret_key': '*Pick a combination of 4 unique digits.',
        }

    def save(self, commit=True):
        # Create the User first
        user = User.objects.create_user(
            username=self.cleaned_data['company_name'],
            password=self.cleaned_data['secret_key']
        )
        organizer = super().save(commit=False)
        organizer.user = user 
        if commit:
            organizer.save()
        return organizer