from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username/Email/Phone", required=True)
    
class SignupForm(UserCreationForm):
    phone_number = forms.CharField(required=True, max_length=15)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'username', 'email', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("A user with this phone number already exists.")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return username