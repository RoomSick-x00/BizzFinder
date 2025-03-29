from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),  # User dashboard or homepage
    path('contactus/', views.contactus, name="contactus"),
    path('categories/', views.categoriesnew, name="categoriesnew"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"), 
    path('hotel/', views.hotel, name="hotel"),
    path('newrestaurant/', views.newrestaurant, name="newrestaurant"),
    path('newretail/', views.newretail, name="newretail"),
    path('newgym/', views.newgym, name="newgym"),
    path('newhospital/', views.newhospital, name="newhospital"),
    path('user/', views.user_view, name="user"),  
    path('profile/', views.profile, name="profile"),  
]
