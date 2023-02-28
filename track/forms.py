from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

from .models import Application, Company

User = get_user_model()


class NewApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['date', 'company', 'position', 'application_amount', 'localization', 'result']
        widgets = {
            'date':  forms.widgets.DateInput(attrs={'type': 'date'})
        }


class UpdateApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['date', 'company', 'position', 'application_amount', 'localization', 'result']
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'})
        }


class NewCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        username = cd.get('username')
        password = cd.get('password')
        self.user = authenticate(username=username, password=password)
        if self.user is None:
            raise ValidationError('Enter a correct data!')
