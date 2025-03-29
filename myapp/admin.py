from django.contrib import admin
from .models import Restaurant, Review, MenuItem, CustomUser

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(MenuItem)
admin.site.register(CustomUser)