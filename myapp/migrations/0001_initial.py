# Generated by Django 5.1.6 on 2025-04-23 17:57

import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('icon', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='restaurants/')),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('website', models.URLField(blank=True, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=3, null=True, validators=[django.core.validators.MaxValueValidator(5.0)])),
                ('review_count', models.PositiveIntegerField(default=0)),
                ('price_range', models.CharField(choices=[('$', 'Budget'), ('$$', 'Moderate'), ('$$$', 'Expensive'), ('$$$$', 'Very Expensive')], default='$$', max_length=10)),
                ('cuisine_type', models.CharField(blank=True, max_length=50)),
                ('opening_hours', models.CharField(blank=True, max_length=200)),
                ('is_featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='Active', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('user', 'User'), ('retailer', 'Retailer')], default='user', max_length=10)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('profile_picture', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('image', models.ImageField(blank=True, null=True, upload_to='menu_items/')),
                ('is_vegetarian', models.BooleanField(default=False)),
                ('is_vegan', models.BooleanField(default=False)),
                ('is_gluten_free', models.BooleanField(default=False)),
                ('category', models.CharField(choices=[('appetizer', 'Appetizer'), ('main', 'Main Course'), ('dessert', 'Dessert'), ('beverage', 'Beverage'), ('side', 'Side Dish')], default='main', max_length=20)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='myapp.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Retailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100)),
                ('business_address', models.TextField()),
                ('business_category', models.CharField(choices=[('restaurant', 'Restaurant'), ('retail', 'Retail Store'), ('gym', 'Gym'), ('hospital', 'Hospital'), ('hotel', 'Hotel')], max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('total_views', models.IntegerField(default=0)),
                ('total_reviews', models.IntegerField(default=0)),
                ('average_rating', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='retailer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='retailer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurants', to='myapp.retailer'),
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='hotels/')),
                ('rating', models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=3, null=True, validators=[django.core.validators.MaxValueValidator(5.0)])),
                ('review', models.TextField(blank=True, max_length=500, null=True)),
                ('price_range', models.CharField(choices=[('$', 'Budget'), ('$$', 'Moderate'), ('$$$', 'Expensive'), ('$$$$', 'Very Expensive')], default='$$', max_length=10)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('website', models.URLField(blank=True, null=True)),
                ('amenities', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='Active', max_length=20)),
                ('retailer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotels', to='myapp.retailer')),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='hospitals/')),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('website', models.URLField(blank=True, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=3, null=True, validators=[django.core.validators.MaxValueValidator(5.0)])),
                ('review_count', models.PositiveIntegerField(default=0)),
                ('specialties', models.TextField(blank=True)),
                ('emergency_services', models.BooleanField(default=True)),
                ('insurance_accepted', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='Active', max_length=20)),
                ('retailer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hospitals', to='myapp.retailer')),
            ],
        ),
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='gyms/')),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('website', models.URLField(blank=True, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=3, null=True, validators=[django.core.validators.MaxValueValidator(5.0)])),
                ('review_count', models.PositiveIntegerField(default=0)),
                ('price_range', models.CharField(choices=[('$', 'Budget'), ('$$', 'Moderate'), ('$$$', 'Expensive'), ('$$$$', 'Very Expensive')], default='$$', max_length=10)),
                ('opening_hours', models.CharField(blank=True, max_length=200)),
                ('facilities', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='Active', max_length=20)),
                ('retailer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gyms', to='myapp.retailer')),
            ],
        ),
        migrations.CreateModel(
            name='RetailStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='retail_stores/')),
                ('rating', models.FloatField(blank=True, default=0.0, null=True, validators=[django.core.validators.MaxValueValidator(5.0)])),
                ('review', models.TextField(blank=True)),
                ('store_type', models.CharField(help_text='e.g., General Store, Electronics, Fashion, etc.', max_length=50)),
                ('operating_hours', models.CharField(help_text="e.g., '9:00 AM - 10:00 PM'", max_length=100)),
                ('payment_methods', models.CharField(help_text="e.g., 'Cash, Card, UPI'", max_length=200)),
                ('address', models.TextField()),
                ('special_offers', models.TextField(blank=True, help_text='Any ongoing offers or discounts')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='Active', max_length=20)),
                ('phone', models.CharField(blank=True, help_text='Contact number of the store', max_length=15, null=True)),
                ('description', models.TextField(blank=True, help_text='Detailed description of the store')),
                ('retailer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='retail_stores', to='myapp.retailer')),
            ],
            options={
                'verbose_name': 'Retail Store',
                'verbose_name_plural': 'Retail Stores',
                'ordering': ['-rating', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_type', models.CharField(blank=True, choices=[('restaurant', 'Restaurant'), ('hotel', 'Hotel'), ('gym', 'Gym'), ('hospital', 'Hospital'), ('retail', 'Retail Store')], max_length=20, null=True)),
                ('business_id', models.IntegerField(blank=True, null=True)),
                ('rating', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=0)),
                ('sent_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_chats', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_chats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
