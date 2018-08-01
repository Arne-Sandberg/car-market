from django import forms


class LoginForms(forms.Form):
    name = 'Log In'
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class SigninForm(forms.Form):
    name = 'Sign In'
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())