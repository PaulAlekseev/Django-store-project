from dataclasses import fields
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=70,
        help_text='Required'
        )

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        user.is_active = False
        if commit:
            user.save()
        return user

