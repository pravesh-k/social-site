from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from .models import Profile

# Form to authenticate users against the database
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)      # the PasswordInput widget renders the 
                                                                # password HTML element.

# Form to create user registration
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User    #using User from auth models
        fields = ('username', 'first_name', 'email')    #filtering the fields to be displayed for user regn
    
    def clean_password2(self):  
        cd = self.cleaned_data  #cleaning data
        if cd['password'] != cd['password2']:   #if password and confirm password do not match, raise alert
            raise forms.ValidationError('\nPasswords do not match.')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User        # importing User form from the django contrib module
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')