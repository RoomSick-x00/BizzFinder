from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from .models import Restaurant, Hotel, Gym, Hospital, RetailStore, Review, Contact, Category, CustomUser, MenuItem
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .forms import CustomLoginForm, CustomProfileEditForm, CustomUserCreationForm

def index(request):
    """Public homepage view"""
    try:
        # Get some featured items to display on homepage
        featured_restaurants = Restaurant.objects.filter(is_featured=True)[:4]
        featured_hotels = Hotel.objects.all()[:4]
        featured_gyms = Gym.objects.all()[:4]
        
        context = {
            'featured_restaurants': featured_restaurants,
            'featured_hotels': featured_hotels,
            'featured_gyms': featured_gyms,
        }
        return render(request, 'index.html', context)
    except Exception as e:
        messages.error(request, 'Error loading homepage. Please try again.')
        return render(request, 'index.html')

def categories(request):
    """Categories view"""
    try:
        categories = [
            {
                'name': 'Hotels',
                'description': 'Find the best hotels and accommodations in your area.',
                'image': 'pictures/hotel main.jpeg',
                'url_name': 'hotel'
            },
            {
                'name': 'Restaurants',
                'description': 'Discover amazing restaurants and cafes near you.',
                'image': 'pictures/restaurant.jpg',
                'url_name': 'restaurant'
            },
            {
                'name': 'Gyms',
                'description': 'Find fitness centers and gyms to stay healthy.',
                'image': 'pictures/infinity.jpg',
                'url_name': 'gym'
            },
            {
                'name': 'Hospitals',
                'description': 'Locate hospitals and healthcare facilities.',
                'image': 'pictures/hospital.jpg',
                'url_name': 'hospital'
            },
            {
                'name': 'Retail Stores',
                'description': 'Shop at the best retail stores in your vicinity.',
                'image': 'pictures/retail store.jpg',
                'url_name': 'retail'
            }
        ]
        return render(request, 'categoriesnew.html', {'categories': categories})
    except Exception as e:
        messages.error(request, 'Error loading categories. Please try again.')
        return render(request, 'categoriesnew.html')

def newrestaurant(request):
    try:
        restaurants = Restaurant.objects.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
        paginator = Paginator(restaurants, 12)
        page = request.GET.get('page')
        try:
            restaurants = paginator.page(page)
        except PageNotAnInteger:
            restaurants = paginator.page(1)
        except EmptyPage:
            restaurants = paginator.page(paginator.num_pages)
        return render(request, 'newrestaurant.html', {'restaurants': restaurants})
    except Exception as e:
        messages.error(request, 'Error loading restaurants. Please try again.')
        return render(request, 'newrestaurant.html', {'restaurants': []})

def hotel(request):
    try:
        hotels = Hotel.objects.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
        paginator = Paginator(hotels, 12)
        page = request.GET.get('page')
        try:
            hotels = paginator.page(page)
        except PageNotAnInteger:
            hotels = paginator.page(1)
        except EmptyPage:
            hotels = paginator.page(paginator.num_pages)
        return render(request, 'hotel.html', {'hotels': hotels})
    except Exception as e:
        messages.error(request, 'Error loading hotels. Please try again.')
        return render(request, 'hotel.html', {'hotels': []})

def newgym(request):
    try:
        gyms = Gym.objects.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
        paginator = Paginator(gyms, 12)
        page = request.GET.get('page')
        try:
            gyms = paginator.page(page)
        except PageNotAnInteger:
            gyms = paginator.page(1)
        except EmptyPage:
            gyms = paginator.page(paginator.num_pages)
        return render(request, 'newgym.html', {'gyms': gyms})
    except Exception as e:
        messages.error(request, 'Error loading gyms. Please try again.')
        return render(request, 'newgym.html', {'gyms': []})

def newhospital(request):
    try:
        hospitals = Hospital.objects.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
        paginator = Paginator(hospitals, 12)
        page = request.GET.get('page')
        try:
            hospitals = paginator.page(page)
        except PageNotAnInteger:
            hospitals = paginator.page(1)
        except EmptyPage:
            hospitals = paginator.page(paginator.num_pages)
        return render(request, 'newhospital.html', {'hospitals': hospitals})
    except Exception as e:
        messages.error(request, 'Error loading hospitals. Please try again.')
        return render(request, 'newhospital.html', {'hospitals': []})

def newretail(request):
    try:
        stores = RetailStore.objects.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
        paginator = Paginator(stores, 12)
        page = request.GET.get('page')
        try:
            stores = paginator.page(page)
        except PageNotAnInteger:
            stores = paginator.page(1)
        except EmptyPage:
            stores = paginator.page(paginator.num_pages)
        return render(request, 'newretail.html', {'stores': stores})
    except Exception as e:
        messages.error(request, 'Error loading retail stores. Please try again.')
        return render(request, 'newretail.html', {'stores': []})

def contactus(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            
            if not all([name, email, message]):
                messages.error(request, 'All fields are required.')
                return render(request, 'contactus.html')
            
            Contact.objects.create(
                name=name,
                email=email,
                message=message
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('index')
        except Exception as e:
            messages.error(request, 'Error sending message. Please try again.')
    
    return render(request, 'contactus.html')

@login_required
def add_review(request):
    if request.method == 'POST':
        try:
            business_type = request.POST.get('business_type')
            business_id = request.POST.get('business_id')
            rating = float(request.POST.get('rating'))
            comment = request.POST.get('comment')
            
            if not all([business_type, business_id, rating, comment]):
                raise ValidationError('All fields are required')
            
            if not 0 <= rating <= 5:
                raise ValidationError('Rating must be between 0 and 5')
            
            Review.objects.create(
                business_type=business_type,
                business_id=business_id,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'Review added successfully!')
            return redirect(request.POST.get('next', 'index'))
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'Error adding review. Please try again.')
    
    return redirect('index')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('index')
            except Exception as e:
                messages.error(request, 'Error creating account. Please try again.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('index')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomProfileEditForm(request.POST, request.FILES, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        
        # Check if any password fields are filled
        new_password = request.POST.get('new_password1', '').strip()
        if new_password:
            # Password change attempted
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password updated successfully!')
                return redirect('profile')
            else:
                for error in password_form.errors.values():
                    messages.error(request, error[0])
        
        # Handle profile updates
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error[0])
    else:
        form = CustomProfileEditForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    
    return render(request, 'edit_profile.html', {
        'form': form,
        'password_form': password_form
    })

def search(request):
    """Search view for all business types"""
    try:
        query = request.GET.get('q', '')
        category = request.GET.get('category', 'all')
        
        if not query:
            return render(request, 'search.html', {'query': query})
        
        # Initialize empty querysets
        restaurants = Restaurant.objects.none()
        hotels = Hotel.objects.none()
        gyms = Gym.objects.none()
        hospitals = Hospital.objects.none()
        retail_stores = RetailStore.objects.none()
        
        # Search based on category
        if category == 'all' or category == 'restaurants':
            restaurants = Restaurant.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(address__icontains=query)
            )
        
        if category == 'all' or category == 'hotels':
            hotels = Hotel.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(address__icontains=query)
            )
            
        if category == 'all' or category == 'gyms':
            gyms = Gym.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(address__icontains=query)
            )
            
        if category == 'all' or category == 'hospitals':
            hospitals = Hospital.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(address__icontains=query)
            )
            
        if category == 'all' or category == 'retail':
            retail_stores = RetailStore.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(address__icontains=query)
            )
        
        context = {
            'query': query,
            'category': category,
            'restaurants': restaurants[:8],
            'hotels': hotels[:8],
            'gyms': gyms[:8],
            'hospitals': hospitals[:8],
            'retail_stores': retail_stores[:8],
            'total_results': (
                restaurants.count() +
                hotels.count() +
                gyms.count() +
                hospitals.count() +
                retail_stores.count()
            )
        }
        
        return render(request, 'search.html', context)
        
    except Exception as e:
        messages.error(request, 'Error performing search. Please try again.')
        return redirect('index')
