from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Repeat Password'}))

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {'placeholder': 'First Name'}
        self.fields['last_name'].widget.attrs = {'placeholder': 'Last Name'}
        self.fields['username'].widget.attrs = {'placeholder': 'Username'}
        self.fields['email'].widget.attrs = {'placeholder': 'Email'}

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['required'] = True

    def clean(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]

        if len(password) < 6:
            self.errors['password'] = 'Password should be at least 6 characters'
            raise forms.ValidationError(
                'Password should be at least 6 characters')

        if password != confirm_password:
            self.errors['password'] = 'Passwords did not match'
            raise forms.ValidationError('Passwords did not match')


class LoginForm(forms.Form):
    username_or_email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Username or Email', 'id': 'usernameOrEmail', 'class': 'form-control', 'required': True}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'id': 'password', 'class': 'form-control', 'required': True}))
