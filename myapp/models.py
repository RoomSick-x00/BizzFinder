from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('user', 'User'),
        ('retailer', 'Retailer'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    profile_picture = models.ImageField(upload_to="profile", blank=True, null=True, default='default.jpg')

    USERNAME_FIELD = "phone_number"  # Login using phone number
    REQUIRED_FIELDS = ["username", "email"]

    def __str__(self):
        return self.phone_number

class Retailer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='retailer')
    business_name = models.CharField(max_length=100)
    business_address = models.TextField()
    business_category = models.CharField(max_length=50, choices=[
        ('restaurant', 'Restaurant'),
        ('retail', 'Retail Store'),
        ('gym', 'Gym'),
        ('hospital', 'Hospital'),
        ('hotel', 'Hotel')
    ])
    phone_number = models.CharField(max_length=15)
    total_views = models.IntegerField(default=0)
    total_reviews = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name

    def update_stats(self):
        self.total_reviews = self.retailer_reviews.count()
        if self.total_reviews > 0:
            self.average_rating = self.retailer_reviews.aggregate(models.Avg('rating'))['rating__avg']
        else:
            self.average_rating = 0.0
        self.save()

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
        validators=[MaxValueValidator(5.0)],
        default=0,
        null=True,
        blank=True
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
    status = models.CharField(max_length=20, default='Active', choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ])
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name='restaurants', null=True, blank=True)

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    BUSINESS_TYPES = [
        ('restaurant', 'Restaurant'),
        ('hotel', 'Hotel'),
        ('gym', 'Gym'),
        ('hospital', 'Hospital'),
        ('retail', 'Retail Store'),
    ]


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    

    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPES, null=True, blank=True)
    business_id = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(validators=[MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.business_type} #{self.business_id}"

    def save(self, *args, **kwargs):
        """Override save method to update business rating."""
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if self.business_type and self.business_id:
            # Get the business model based on business_type
            business_model = None
            if self.business_type == 'restaurant':
                business_model = Restaurant
            elif self.business_type == 'hotel':
                business_model = Hotel
            elif self.business_type == 'gym':
                business_model = Gym
            elif self.business_type == 'hospital':
                business_model = Hospital
            elif self.business_type == 'retail':
                business_model = RetailStore

            if business_model:
                try:
                    business = business_model.objects.get(id=self.business_id)
                    reviews = Review.objects.filter(
                        business_type=self.business_type,
                        business_id=self.business_id
                    )

                    # Update review count and average rating
                    business.review_count = reviews.count()
                    if business.review_count > 0:
                        avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
                        business.rating = round(avg_rating, 1)
                    else:
                        business.rating = 0

                    business.save()
                except business_model.DoesNotExist:
                    pass  # Handle the case where business doesn't exist


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
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MaxValueValidator(5.0)],
        default=0,
        null=True,
        blank=True
    )
    review = models.TextField(max_length=500, blank=True, null=True)
    price_range = models.CharField(max_length=20, choices=Restaurant.PRICE_CHOICES, default='$$')
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    amenities = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='Active', choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ])
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name='hotels', null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def rating_range(self):
        """Returns a range of 5 for star display"""
        return range(1, 6)


class RetailStore(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='retail_stores/', blank=True, null=True)
    rating = models.FloatField(
        default=0.0,
        validators=[MaxValueValidator(5.0)],
        null=True,
        blank=True
    )
    review = models.TextField(blank=True)
    store_type = models.CharField(max_length=50, help_text="e.g., General Store, Electronics, Fashion, etc.")
    operating_hours = models.CharField(max_length=100, help_text="e.g., '9:00 AM - 10:00 PM'")
    payment_methods = models.CharField(max_length=200, help_text="e.g., 'Cash, Card, UPI'")
    address = models.TextField()
    special_offers = models.TextField(blank=True, help_text="Any ongoing offers or discounts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='Active', choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ])
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name='retail_stores', null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True, help_text="Contact number of the store")
    description = models.TextField(blank=True, help_text="Detailed description of the store")

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
        validators=[MaxValueValidator(5.0)],
        default=0,
        null=True,
        blank=True
    )
    review_count = models.PositiveIntegerField(default=0)
    price_range = models.CharField(max_length=10, choices=Restaurant.PRICE_CHOICES, default='$$')
    opening_hours = models.CharField(max_length=200, blank=True)
    facilities = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='Active', choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ])
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name='gyms', null=True, blank=True)

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
        validators=[MaxValueValidator(5.0)],
        default=0,
        null=True,
        blank=True
    )
    review_count = models.PositiveIntegerField(default=0)
    specialties = models.TextField(blank=True)
    emergency_services = models.BooleanField(default=True)
    insurance_accepted = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='Active', choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ])
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name='hospitals', null=True, blank=True)

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

@receiver(post_save, sender=settings.AUTH_USER_MODEL)

def create_vendor_profile(sender, instance, created, **kwargs):
    if created and hasattr(instance, 'user_type') and instance.user_type == 'vendor':
        Vendor.objects.create(user=instance)


class UserChat(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_chats')
    sent_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_chats')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)  # 0=unread, 1=read

def create_retailer_profile(sender, instance, created, **kwargs):
    if created and hasattr(instance, 'user_type') and instance.user_type == 'retailer':
        Retailer.objects.create(user=instance)

