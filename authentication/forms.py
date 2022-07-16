from dataclasses import fields
from django import forms
from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Enter username',
        min_length=4,
        max_length=50,
        help_text='Required'
        )
    email = forms.EmailField(
        max_length=70,
        help_text='Required'
        )
    password = forms.CharField(label='Password')
    password2 = forms.CharField(label='Repeat your password')

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
    

    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = CustomUser.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email
    