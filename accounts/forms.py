from django import forms
from .models import User, UserProfile, ShippingAddress
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


from django.core.exceptions import ValidationError
from django.utils import timezone

class UserRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "date_of_birth", "password1", "password2"]

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get("date_of_birth")
        if dob and dob > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future.")
        return dob

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if not first_name:
            self.add_error("first_name", "First name is required.")
        if not last_name:
            self.add_error("last_name", "Last name is required.")
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "date_of_birth"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "profile_picture"]

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ["street", "city", "state_or_province", "postal_code"]