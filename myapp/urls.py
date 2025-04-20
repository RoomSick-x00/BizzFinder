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
    path('retailer/', views.retailer, name="retailer"),
    path('add-review/<str:business_type_param>/<int:business_id>/', views.add_review, name='add_review'),
    path('add-business/', views.add_business, name="add_business"),
    path('business-search/', views.business_search, name='business_search'),
    path('item-search/', views.item_search, name='item_search'),
    path('edit-business/<str:business_type>/<int:business_id>/', views.edit_business, name='edit_business'),
    # path('api/get-business-details/<str:business_type>/<int:business_id>/', views.get_business_details, name='get_business_details'),
    path('interaction/', views.interaction, name='interaction'),
]
