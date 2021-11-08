from django import forms

# Form to authenticate users against the database
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)      # the PasswordInput widget renders the 
                                                                # password HTML element.