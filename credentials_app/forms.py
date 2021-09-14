from django import forms
from .models import Account
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

non_allowed_usernames = ['Sarvesh']
User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "confirm-user-password"
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact = username)
        if username in non_allowed_usernames:
            raise forms.ValidationError("User Already Exists")
        if qs.exists():
            raise forms.ValidationError("User Already Exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact = email)
        if qs.exists():
            raise forms.ValidationError("Email is already in Use")
        return email


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
            'email',
        ]


class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'platform',
            'username',
            'password',
            'email',
            'mobile'
        ]


class ModifyAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'platform',
            'username',
            'password',
            'email',
            'mobile'
        ]