from django.test import TestCase, override_settings
from django.urls import reverse, resolve
from myapp.models import CustomUser, Retailer
from myapp.forms import CustomUserCreationForm
from myapp.views import signup
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.

class ModelTests(TestCase):
    def setUp(self):
        # Create test data
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

    def test_custom_user_creation(self):
        """Test that a custom user is created correctly."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')

    def test_retailer_creation(self):
        """Test that a retailer profile is created correctly."""
        retailer = Retailer.objects.create(
            user=self.user,
            business_name='Test Business',
            business_address='123 Test St',
            business_category='restaurant',
            phone_number='1234567890'
        )
        self.assertEqual(retailer.business_name, 'Test Business')
        self.assertEqual(retailer.phone_number, '1234567890')

    def test_unique_username(self):
        """Test that usernames must be unique."""
        with self.assertRaises(Exception):  # Expect an IntegrityError
            CustomUser.objects.create_user(
                username='testuser',  # Duplicate username
                email='another@example.com',
                password='password123'
            )


@override_settings(AUTH_PASSWORD_VALIDATORS=[])
class FormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123',
            'phone_number': '1234567890',
            'user_type': 'user',  # Required field
        }
        form = CustomUserCreationForm(data=form_data)
        if not form.is_valid():
            print(form.errors)  # Debugging: Print validation errors
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Test that the form is invalid with incorrect data."""
        form_data = {
            'username': '',  # Invalid: Empty username
            'email': 'invalid-email',  # Invalid email format
            'password1': 'password123',
            'password2': 'mismatched-password',
            'phone_number': '1234567890',
            'user_type': 'user',  # Required field
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)


class ViewTests(TestCase):
    def test_signup_page_loads(self):
        """Test that the signup page loads successfully."""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_valid_user_signup(self):
        """Test that a valid user signup creates a user and redirects."""
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
            'phone_number': '1234567890',
            'user_type': 'user', 
        })
        if response.status_code != 302:
            print(response.context['form'].errors)
        self.assertRedirects(response, reverse('login'))  # Successful signup redirects to login
        self.assertEqual(CustomUser.objects.count(), 1)  # Ensure user was created
        self.assertEqual(Retailer.objects.count(), 0)  # No retailer should be created

    def test_valid_retailer_signup(self):
        """Test that a valid retailer signup creates a user and retailer profile."""
        response = self.client.post(reverse('signup'), {
            'username': 'retailertest',
            'email': 'retailer@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
            'phone_number': '9876543210',
            'user_type': 'retailer',  # Retailer signup
            'business_name': 'Test Business',
            'business_address': '123 Vendor St',
            'business_category': 'restaurant',
        })
        if response.status_code != 302:
            print(response.context['forms'].errors)
            print(response.content.decode()) 
    def test_valid_retailer_signup(self):
        """Test that a valid retailer signup creates a user and retailer profile."""
        response = self.client.post(reverse('signup'), {
            'username': 'retailertest',
            'email': 'retailer@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
            'phone_number': '9876543210',
            'user_type': 'retailer',  # Retailer signup
            'business_name': 'Test Business',
            'business_address': '123 Vendor St',
            'business_category': 'restaurant',
        })
        if response.status_code != 302:
            print(response.context['form'].errors)
            print(response.content.decode()) 
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(CustomUser.objects.count(), 1)  
        self.assertEqual(Retailer.objects.count(), 1)
        
        retailer = Retailer.objects.first()
        self.assertEqual(retailer.business_name, 'Test Business')
        self.assertEqual(retailer.business_address, '123 Vendor St')
        self.assertEqual(retailer.business_category, 'restaurant')

        # Check that a CustomUser object was created
        self.assertEqual(CustomUser.objects.count(), 1)
        user = CustomUser.objects.first()
        self.assertEqual(user.username, 'retailertest')
        self.assertEqual(user.email, 'retailer@example.com')

        # Check that a Retailer object was created
        self.assertEqual(Retailer.objects.count(), 1)
        retailer = Retailer.objects.first()
        self.assertEqual(retailer.user, user)
        self.assertEqual(retailer.business_name, 'Test Business')
        self.assertEqual(retailer.business_address, '123 Vendor St')
        self.assertEqual(retailer.business_category, 'restaurant')
        self.assertEqual(retailer.phone_number, '9876543210')

    def test_invalid_signup(self):
        """Test that an invalid signup re-renders the form with errors."""
        response = self.client.post(reverse('signup'), {
            'username': '',
            'email': 'invalid-email',
            'password1': 'password123',
            'password2': 'mismatched-password',
            'phone_number': '1234567890',
            'user_type': 'user',  # Required field
        })
        self.assertEqual(response.status_code, 200)  # Form should re-render with errors
        self.assertContains(response, 'This field is required.')  # Error message for empty username
        self.assertContains(response, 'Enter a valid email address.')  # Error message for invalid email


class URLTests(TestCase):
    def test_signup_url_resolves(self):
        """Test that the signup URL resolves to the correct view."""
        url = reverse('signup')
        self.assertEqual(resolve(url).func, signup)

    def test_login_url_resolves(self):
        """Test that the login URL resolves to the correct view."""
        url = reverse('login')
        from myapp.views import login_view  # Adjust the import as needed
        self.assertEqual(resolve(url).func, login_view)