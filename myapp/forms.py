from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser, Retailer

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username/Email/Phone", required=True)
    
class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)

    # Retailer fields
    business_name = forms.CharField(max_length=100, required=False)
    business_address = forms.CharField(widget=forms.Textarea, required=False)
    business_category = forms.ChoiceField(choices=[
        ('restaurant', 'Restaurant'),
        ('retail', 'Retail Store'),
        ('gym', 'Gym'),
        ('hospital', 'Hospital'),
        ('hotel', 'Hotel')
    ], required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number', 'email', 'password1', 'password2',
                  'business_name', 'business_address', 'business_category')
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone_number


class SignupForm(UserCreationForm):
    phone_number = forms.CharField(required=True, max_length=10)  # Ensure 10 digits
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'username', 'email', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Check if phone number is numeric and is 10 digits long
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        
        # Check if phone number already exists
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("A user with this phone number already exists.")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username

class CustomProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make profile picture optional
        self.fields['profile_picture'].required = False
        
        # Make username optional and readonly if already set
        if self.instance and self.instance.username:
            self.fields['username'].required = False
            self.fields['username'].widget.attrs['readonly'] = True
        
        # Make email readonly and not required if already set
        if self.instance and self.instance.email:
            self.fields['email'].required = False
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['disabled'] = True
            
    def clean_email(self):
        # Always return the instance email if it exists
        if self.instance and self.instance.email:
            return self.instance.email
        return self.cleaned_data.get('email')
        
    def clean_username(self):
        # Always return the instance username if it exists
        if self.instance and self.instance.username:
            return self.instance.username
        return self.cleaned_data.get('username')

class RetailerSignupForm(UserCreationForm):
    business_name = forms.CharField(max_length=100)
    business_address = forms.CharField(widget=forms.Textarea)
    business_category = forms.ChoiceField(choices=[
        ('restaurant', 'Restaurant'),
        ('retail', 'Retail Store'),
        ('gym', 'Gym'),
        ('hospital', 'Hospital'),
        ('hotel', 'Hotel')
    ])
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'business_name', 
                 'business_address', 'business_category', 'phone_number')

class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = Retailer
        fields = ['business_name', 'business_address', 'business_category']
        widgets = {
            'business_address': forms.Textarea(attrs={'rows': 3}),
        }
        
class BusinessSearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('', 'All Categories'),
        ('restaurant', 'Restaurant'),
        ('hotel', 'Hotel'),
        ('gym', 'Gym'),
        ('hospital', 'Hospital'),
        ('retail', 'Retail Store'),
    ]
    
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)
    location = forms.CharField(max_length=100, required=False)

class ItemSearchForm(forms.Form):
    item_name = forms.CharField(max_length=100, required=True)
    location = forms.CharField(max_length=100, required=False)