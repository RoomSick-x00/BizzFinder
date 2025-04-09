from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),  # Public homepage
    path('search/', views.search, name="search"),  # Add search URL
    path('contactus/', views.contactus, name="contactus"),
    path('categories/', views.categories, name="categories"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('hotel/', views.hotel, name="hotel"),
    path('gym/', views.newgym, name="gym"),
    path('hospital/', views.newhospital, name="hospital"),
    path('restaurant/', views.newrestaurant, name="restaurant"),
    path('retail/', views.newretail, name="retail"),
    path('profile/', views.profile_view, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('signup/', views.signup, name="signup"),
    path('add-review/<int:business_id>/', views.add_review, name="add_review"),
]
