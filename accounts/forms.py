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
        fields = ["first_name", "last_name", "email", "phone_number"]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-white transition-colors text-white',
                'placeholder': 'Nombre',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-white transition-colors text-white',
                'placeholder': 'Apellido',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-white transition-colors text-white',
                'placeholder': 'Email',
                'required': True
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-white transition-colors text-white',
                'placeholder': 'Teléfono',
                'required': True
            }),
        }
    
    def clean_first_name(self):
        """Validar que el nombre no esté vacío"""
        first_name = self.cleaned_data.get('first_name')
        if not first_name or first_name.strip() == '':
            raise ValidationError('El nombre es obligatorio')
        return first_name
    
    def clean_last_name(self):
        """Validar que el apellido no esté vacío"""
        last_name = self.cleaned_data.get('last_name')
        if not last_name or last_name.strip() == '':
            raise ValidationError('El apellido es obligatorio')
        return last_name
    
    def clean_phone_number(self):
        """Validar que el teléfono no esté vacío"""
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number or phone_number.strip() == '':
            raise ValidationError('El teléfono es obligatorio')
        return phone_number


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "profile_picture"]
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-white transition-colors text-white',
                'placeholder': 'Cuéntanos sobre ti...'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-white transition-colors text-white'
            }),
        }

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ["street", "city", "state_or_province", "postal_code"]