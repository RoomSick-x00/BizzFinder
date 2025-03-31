from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    profile_picture = models.ImageField(upload_to="profile", blank=True, null=True)

    USERNAME_FIELD = "phone_number"  # Login using phone number
    REQUIRED_FIELDS = ["username", "email"]

    def __str__(self):
        return self.phone_number


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)

    # Updated rating field to avoid decimal rounding issues
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        default=0
    )
    review_count = models.PositiveIntegerField(default=0)

    # Price range options
    PRICE_CHOICES = [
        ('$', 'Budget'),
        ('$$', 'Moderate'),
        ('$$$', 'Expensive'),
        ('$$$$', 'Very Expensive'),
    ]
    price_range = models.CharField(max_length=10, choices=PRICE_CHOICES, default='$$')

    cuisine_type = models.CharField(max_length=50, blank=True)
    opening_hours = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def stars_display(self):
        """Returns a string representation of stars based on rating."""
        full_stars = int(self.rating)
        half_star = '½' if self.rating % 1 >= 0.5 else ''
        empty_stars = '☆' * (5 - full_stars - (1 if half_star else 0))
        return '★' * full_stars + half_star + empty_stars


# ✅ Review Model
class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    author_name = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.author_name} for {self.restaurant.name}"

    def save(self, *args, **kwargs):
        """Override save method to update restaurant rating."""
        is_new = self.pk is None
        super().save(*args, **kwargs)

        restaurant = self.restaurant
        reviews = restaurant.reviews.all()
        restaurant.review_count = reviews.count()

        if restaurant.review_count > 0:
            total_rating = sum(review.rating for review in reviews)
            restaurant.rating = total_rating / restaurant.review_count
        else:
            restaurant.rating = None  # Set to None if no reviews

        restaurant.save()


# ✅ Menu Item Model
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)

    CATEGORY_CHOICES = [
        ('appetizer', 'Appetizer'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
        ('side', 'Side Dish'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='main')

    def __str__(self):
        return f"{self.name} at {self.restaurant.name}"


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    image_url = models.CharField(max_length=200)  
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        default=0
    )
    review = models.TextField(max_length=500)
    price_range = models.CharField(max_length=10, choices=Restaurant.PRICE_CHOICES, default='$$')
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    amenities = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def rating_range(self):
        """Returns a range of 5 for star display"""
        return range(1, 6)


class RetailStore(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='retail_stores/')
    rating = models.FloatField(default=0.0)
    review = models.TextField(blank=True)
    store_type = models.CharField(max_length=50, help_text="e.g., General Store, Electronics, Fashion, etc.")
    operating_hours = models.CharField(max_length=100, help_text="e.g., '9:00 AM - 10:00 PM'")
    payment_methods = models.CharField(max_length=200, help_text="e.g., 'Cash, Card, UPI'")
    address = models.TextField()
    special_offers = models.TextField(blank=True, help_text="Any ongoing offers or discounts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Retail Store"
        verbose_name_plural = "Retail Stores"
        ordering = ['-rating', '-created_at']


class Gym(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='gyms/', blank=True, null=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        default=0
    )
    review_count = models.PositiveIntegerField(default=0)
    price_range = models.CharField(max_length=10, choices=Restaurant.PRICE_CHOICES, default='$$')
    opening_hours = models.CharField(max_length=200, blank=True)
    facilities = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='hospitals/', blank=True, null=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        default=0
    )
    review_count = models.PositiveIntegerField(default=0)
    specialties = models.TextField(blank=True)
    emergency_services = models.BooleanField(default=True)
    insurance_accepted = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
