from django import forms
from .models import User, UserProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "name", "phone_number", "shipping_address", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name","phone_number","shipping_address"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "profile_picture"]
