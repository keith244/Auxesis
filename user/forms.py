from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
import re
from squad.models import Squad

class UserRegistrationForm(UserCreationForm):
    squad = forms.ModelChoiceField(queryset=Squad.objects.all(),required=False)
    role = forms.ChoiceField(choices = Profile.ROLE_CHOICES)
    phone = forms.RegexField(
        regex=r'^\+?\(?\d{1,4}\)?[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{1,4}[\s\-]?\d{1,4}$',
        error_messages={
            'invalid': 'Enter a valid phone number (digits only, with optional + at the beginning).'
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email','phone', 'password1', 'password2', 'role', 'squad')
    
    def save (self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = Profile(user=user)
            profile.role = self.cleaned_data.get('role')
            profile.phone = self.cleaned_data.get('phone')
            profile.save()
        return user

class LoginForm (forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)