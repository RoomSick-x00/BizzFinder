from django.contrib import admin
from .models import Restaurant, Review, MenuItem, CustomUser, Hotel, RetailStore, Gym, Hospital, Contact, Category

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(MenuItem)
admin.site.register(CustomUser)
admin.site.register(Hotel)
admin.site.register(RetailStore)
admin.site.register(Gym)
admin.site.register(Hospital)
admin.site.register(Contact)
admin.site.register(Category)