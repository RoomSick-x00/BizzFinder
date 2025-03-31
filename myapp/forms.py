from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username/Email/Phone", required=True)
    
class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number', 'email', 'password1', 'password2')

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

class CustomProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required
        self.fields['email'].required = True
        # Make profile picture optional
        self.fields['profile_picture'].required = False
        
        # Make email readonly if already set
        if self.instance and self.instance.email:
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['disabled'] = True
            
    def clean_email(self):
        # If email is already set, return the original email
        if self.instance and self.instance.email:
            return self.instance.email
        return self.cleaned_data.get('email')