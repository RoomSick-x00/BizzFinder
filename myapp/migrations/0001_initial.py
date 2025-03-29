# Generated by Django 5.1.6 on 2025-03-19 16:41

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=2, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5)])),
                ('review_count', models.PositiveIntegerField(default=0)),
                ('price_range', models.CharField(choices=[('$', 'Budget'), ('$$', 'Moderate'), ('$$$', 'Expensive'), ('$$$$', 'Very Expensive')], default='$$', max_length=10)),
                ('cuisine_type', models.CharField(blank=True, max_length=50)),
                ('opening_hours', models.CharField(blank=True, max_length=200)),
                ('is_featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
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
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=100)),
                ('comment', models.TextField()),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='myapp.restaurant')),
            ],
        ),
    ]
