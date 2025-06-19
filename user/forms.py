from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
import re
from squad.models import HarvestGroup

class UserRegistrationForm(UserCreationForm):
    # harvest_group = forms.ModelChoiceField(queryset=HarvestGroup.objects.all(),required=False)
    role = forms.ChoiceField(choices = Profile.ROLE_CHOICES) 
    phone = forms.RegexField(
        regex=r'^\+?\(?\d{1,4}\)?[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{1,4}[\s\-]?\d{1,4}$',
        error_messages={
            'invalid': 'Enter a valid phone number (digits only, with optional + at the beginning).'
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email','phone', 'password1', 'password2', 'role', ) #'harvest_group')
    
    def save (self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = Profile(user=user)
            profile.role = self.cleaned_data.get('role') # type: ignore
            profile.phone = self.cleaned_data.get('phone') # type: ignore
            profile.save()
        return user
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        # harvest_group = cleaned_data.get('harvest_group')
        
        if not role:# == 'SHEPHERD' and not harvest_group:
            # raise forms.ValidationError('Shepherds must be assigned to a Harvest Group.')
            raise forms.ValidationError('Choose a position.')
        
        return cleaned_data

class LoginForm (forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)