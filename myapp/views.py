from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from .models import Restaurant, Hotel, Gym, Hospital, RetailStore, Review, Contact, Category, CustomUser, MenuItem, Retailer
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .forms import CustomLoginForm, CustomProfileEditForm, CustomUserCreationForm, ItemSearchForm, BusinessSearchForm

@login_required
def retailer(request):
    # Fetch the retailer associated with the current user
    current_user = request.user
    retailer = get_object_or_404(Retailer, user=current_user)

    # Fetch businesses of all types belonging to this retailer
    restaurants = Restaurant.objects.filter(retailer=retailer)
    hotels = Hotel.objects.filter(retailer=retailer)
    gyms = Gym.objects.filter(retailer=retailer)
    hospitals = Hospital.objects.filter(retailer=retailer)
    retail_stores = RetailStore.objects.filter(retailer=retailer)
    
    # Combine all businesses into one list with proper type information
    businesses = []
    
    for restaurant in restaurants:
        businesses.append({
            'id': restaurant.id,
            'name': restaurant.name,
            'category': 'restaurant',
            'display_category': 'Restaurant',
            'address': restaurant.address,
            'phone': restaurant.phone,
            'status': restaurant.status,
            'model_type': 'restaurant'
        })
    
    for hotel in hotels:
        businesses.append({
            'id': hotel.id,
            'name': hotel.name,
            'category': 'hotel',
            'display_category': 'Hotel',
            'address': hotel.address,
            'phone': hotel.phone,
            'status': hotel.status,
            'model_type': 'hotel'
        })
    
    for gym in gyms:
        businesses.append({
            'id': gym.id,
            'name': gym.name,
            'category': 'gym',
            'display_category': 'Gym',
            'address': gym.address,
            'phone': gym.phone,
            'status': gym.status,
            'model_type': 'gym'
        })
    
    for hospital in hospitals:
        businesses.append({
            'id': hospital.id,
            'name': hospital.name,
            'category': 'hospital',
            'display_category': 'Hospital',
            'address': hospital.address,
            'phone': hospital.phone,
            'status': hospital.status,
            'model_type': 'hospital'
        })
    
    for store in retail_stores:
        businesses.append({
            'id': store.id,
            'name': store.name,
            'category': 'retail',
            'display_category': 'Retail Store',
            'address': store.address,
            'phone': getattr(store, 'phone', store.payment_methods if hasattr(store, 'payment_methods') else ''),
            'status': store.status,
            'model_type': 'retail'
        })

    return render(request, 'retailer/retailer.html', {
        'retailer': retailer,
        'businesses': businesses
    })
    
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
        restaurants = Restaurant.objects.all().order_by('-created_at')
        total_count = restaurants.count()
        
        # For each restaurant, get its top and least rated reviews
        for restaurant in restaurants:
            reviews = Review.objects.filter(
                business_type='restaurant',
                business_id=restaurant.id
            ).order_by('-rating', '-created_at')  # First sort by rating, then by date
            
            # Get top rated review
            restaurant.top_review = reviews.first()
            
            # Get least rated review
            restaurant.least_review = reviews.order_by('rating', '-created_at').first()
        
        paginator = Paginator(restaurants, 12)
        page = request.GET.get('page', 1)
        try:
            paginated_restaurants = paginator.page(page)
        except PageNotAnInteger:
            paginated_restaurants = paginator.page(1)
        except EmptyPage:
            paginated_restaurants = paginator.page(paginator.num_pages)
        
        context = {
            'restaurants': paginated_restaurants,
            'total_count': total_count,
            'is_authenticated': request.user.is_authenticated,
            'current_user': request.user.phone_number if request.user.is_authenticated else "Guest",
        }
        
        return render(request, 'newrestaurant.html', context)
    except Exception as e:
        print(f"Error in restaurant view: {str(e)}")  # For debugging
        return render(request, 'newrestaurant.html', {
            'restaurants': [],
            'total_count': 0,
            'error': str(e),
            'is_authenticated': request.user.is_authenticated,
            'current_user': request.user.phone_number if request.user.is_authenticated else "Guest",
        })


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
        gyms = Gym.objects.all().order_by('-rating')
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
        hospitals = Hospital.objects.all().order_by('-rating')
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
        # Create a test store if none exist
        if RetailStore.objects.count() == 0:
            test_store = RetailStore.objects.create(
                name='Test Store',
                store_type='General Store',
                operating_hours='9 AM - 9 PM',
                payment_methods='Cash, Card',
                address='123 Test Street'
            )
            print(f"Debug - Created test store: {test_store.name}")
        
        # Get all stores
        stores = RetailStore.objects.all()
        print(f"Debug - All stores: {[{'name': store.name, 'rating': store.rating} for store in stores]}")
        return render(request, 'newretail.html', {'stores': stores})
    except Exception as e:
        print(f"Debug - Error in newretail view: {str(e)}")
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
def add_review(request, business_id=None, business_type_param=None):
    # Use the business_type_param if provided
    business_type = business_type_param
    business = None
    
    # Find the business based on type and ID
    if business_type == 'restaurant':
        business = get_object_or_404(Restaurant, id=business_id)
    elif business_type == 'hotel':
        business = get_object_or_404(Hotel, id=business_id)
    elif business_type == 'gym':
        business = get_object_or_404(Gym, id=business_id)
    elif business_type == 'hospital':
        business = get_object_or_404(Hospital, id=business_id)
    elif business_type == 'retail':
        business = get_object_or_404(RetailStore, id=business_id)
    else:
        # Fallback to your old method if type not specified
        if Restaurant.objects.filter(id=business_id).exists():
            business = Restaurant.objects.get(id=business_id)
            business_type = 'restaurant'
        elif Hotel.objects.filter(id=business_id).exists():
            business = Hotel.objects.get(id=business_id)
            business_type = 'hotel'
        elif Gym.objects.filter(id=business_id).exists():
            business = Gym.objects.get(id=business_id)
            business_type = 'gym'
        elif Hospital.objects.filter(id=business_id).exists():
            business = Hospital.objects.get(id=business_id)
            business_type = 'hospital'
        elif RetailStore.objects.filter(id=business_id).exists():
            business = RetailStore.objects.get(id=business_id)
            business_type = 'retail'
    
    # If no valid business or type is found, return an error
    if not business or not business_type:
        messages.error(request, 'Business not found')
        return redirect('index')
    
    # Handle POST request (submitting a review)
    if request.method == 'POST':
        try:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            
            # Validate inputs
            if not all([rating, comment]):
                raise ValidationError('All fields are required')
            
            try:
                rating = int(rating)  # Convert rating to integer
                if not 1 <= rating <= 5:
                    raise ValidationError('Rating must be between 1 and 5')
            except ValueError:
                raise ValidationError('Invalid rating value')
            
            # Create the review
            Review.objects.create(
                user=request.user,
                business_type=business_type,
                business_id=business_id,
                rating=rating,
                comment=comment
            )
            
            # Success message and redirect
            messages.success(request, 'Review added successfully!')
            return redirect(business_type)  # Redirect to the business-specific page
            
        except ValidationError as e:
            messages.error(request, str(e))  # Display validation error
        except Exception as e:
            print(f"Error in add_review: {str(e)}")  # Log unexpected errors
            messages.error(request, 'Error adding review. Please try again.')
    
    # For GET requests or if there's an error in POST
    context = {
        'business': business,
        'business_id': business_id,
        'business_type': business_type
    }
    return render(request, 'add_review.html', context)

def signup(request):
    # Get user_type from query parameters or default to 'user'
    user_type = request.GET.get('type', 'user')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save the user but don't commit yet
                user = form.save(commit=False)
                
                # Update the user_type based on the submitted form
                if request.POST.get('user_type') == 'retailer':
                    user.user_type = 'retailer'  # Set user_type to retailer
                
                # Now save the user with the updated user_type
                user.save()
                
                phone_number = form.cleaned_data.get('phone_number')

                # Check if the user is signing up as a retailer
                if request.POST.get('user_type') == 'retailer':
                    # Create retailer profile
                    Retailer.objects.create(
                        user=user,
                        business_name=form.cleaned_data.get('business_name'),
                        business_address=form.cleaned_data.get('business_address'),
                        business_category=form.cleaned_data.get('business_category'),
                        phone_number=phone_number,
                    )
                
                user.backend = 'django.contrib.auth.backends.ModelBackend' 

                # Log in the user and redirect
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('login')  # Redirect to login page
            except Exception as e:
                # Log the exception for debugging
                print(f"Error during signup: {e}")
                messages.error(request, 'Error creating account. Please try again.')
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    # Render the signup page with the form and user_type
    return render(request, 'signup.html', {
        'form': form,
        'user_type': user_type,
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                if hasattr(user, 'retailer'):  
                    messages.success(request, 'Welcome Retailer!')
                    return redirect('retailer') 
                else:
                    messages.success(request, 'Successfully logged in!')
                    return redirect('profile')  # fallback for regular users

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
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            
            new_password = request.POST.get('new_password1', '').strip()
            if new_password:
                password_form = PasswordChangeForm(request.user, request.POST)
                if password_form.is_valid():
                    user = password_form.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Password updated successfully!')
                else:
                    for error in password_form.errors.values():
                        messages.error(request, error[0])
                    return render(request, 'edit_profile.html', {
                        'form': form,
                        'password_form': password_form
                    })
            
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error[0])
            password_form = PasswordChangeForm(request.user)
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

@login_required
def add_business(request):
    if request.method == 'POST':
        retailer = Retailer.objects.get(user=request.user)
        category = request.POST.get('category')
        name = request.POST.get('name')
        location = request.POST.get('location')
        contact = request.POST.get('contact')
        description = request.POST.get('description')

        if category == 'restaurant':
            cuisine_type = request.POST.get('cuisine_type')
            price_range = request.POST.get('price_range')
            opening_hours = request.POST.get('opening_hours')
            Restaurant.objects.create(
                name=name,
                address=location,
                phone=contact,
                description=description,
                cuisine_type=cuisine_type,
                price_range=price_range,
                opening_hours=opening_hours,
                retailer=retailer
            )
            
        elif category == 'hotel':
            amenities = request.POST.get('amenities')
            price_range = request.POST.get('price_range')
            Hotel.objects.create(
                name=name,
                address=location,
                phone=contact,
                description=description,
                amenities=amenities,
                price_range=price_range,
                retailer=retailer
            )   
            
        elif category == 'gym':
            facilities = request.POST.get('facilities')
            opening_hours = request.POST.get('opening_hours')
            Gym.objects.create(
                name=name,
                address=location,
                phone=contact,
                description=description,
                facilities=facilities,
                opening_hours=opening_hours,
                retailer=retailer
            )
            
        elif category == 'retail':
            store_type = request.POST.get('store_type')
            operating_hours = request.POST.get('operating_hours')
            RetailStore.objects.create(
                name=name,
                address=location,
                phone=contact,
                description=description,
                store_type=store_type,
                operating_hours=operating_hours,
                retailer=retailer
            )
            
        elif category == 'hospital':
            specialties = request.POST.get('specialties')
            emergency_services = request.POST.get('emergency_services') == 'Yes'
            Hospital.objects.create(
                name=name,
                address=location,
                phone=contact,
                description=description,
                specialties=specialties,
                emergency_services=emergency_services,
                retailer=retailer
            )
        messages.success(request, f"{category.capitalize()} added successfully!")
        return redirect('retailer')  # Redirect to the retailer dashboard

    return render(request, 'retailer/retailer.html')


# views.py (add these functions)

def business_search(request):
    """Search view for businesses by category and location"""
    category = request.GET.get('category', '')
    location = request.GET.get('location', '')
    
    # Initialize empty querysets
    restaurants = Restaurant.objects.none()
    hotels = Hotel.objects.none()
    gyms = Gym.objects.none()
    hospitals = Hospital.objects.none()
    retail_stores = RetailStore.objects.none()
    
    # Apply location filter if provided
    location_filter = Q(address__icontains=location) if location else Q()
    
    # Search based on category
    if not category or category == 'restaurant':
        restaurants = Restaurant.objects.filter(location_filter)
    
    if not category or category == 'hotel':
        hotels = Hotel.objects.filter(location_filter)
    
    if not category or category == 'gym':
        gyms = Gym.objects.filter(location_filter)
    
    if not category or category == 'hospital':
        hospitals = Hospital.objects.filter(location_filter)
    
    if not category or category == 'retail':
        retail_stores = RetailStore.objects.filter(location_filter)
    
    context = {
        'category': category,
        'location': location,
        'restaurants': restaurants,
        'hotels': hotels,
        'gyms': gyms,
        'hospitals': hospitals,
        'retail_stores': retail_stores,
        'search_form': BusinessSearchForm(initial={'category': category, 'location': location}),
        'total_results': (
            restaurants.count() +
            hotels.count() +
            gyms.count() +
            hospitals.count() +
            retail_stores.count()
        )
    }
    
    return render(request, 'business_search_results.html', context)

def item_search(request):
    """Search for items across all businesses"""
    item_name = request.GET.get('item_name', '')
    location = request.GET.get('location', '')
    
    if not item_name:
        return render(request, 'item_search_results.html', {
            'item_name': '',
            'location': '',
            'search_form': ItemSearchForm(),
            'results': [],
            'total_results': 0
        })
    
    # Base query for finding items containing the search term
    item_filter = Q(name__icontains=item_name)
    
    # Location filter to apply to businesses if location is provided
    location_filter = Q(restaurant__address__icontains=location) if location else Q()
    
    # Search for menu items in restaurants
    menu_items = MenuItem.objects.filter(item_filter)
    
    # Apply location filter if provided
    if location:
        menu_items = menu_items.filter(restaurant__address__icontains=location)
    
    # Group results by business
    results = []
    
    # Group menu items by restaurant
    restaurants_with_items = {}
    for item in menu_items:
        if item.restaurant not in restaurants_with_items:
            restaurants_with_items[item.restaurant] = []
        restaurants_with_items[item.restaurant].append(item)
    
    # Format results
    for restaurant, items in restaurants_with_items.items():
        results.append({
            'business': restaurant,
            'business_type': 'restaurant',
            'items': items
        })
    
    context = {
        'item_name': item_name,
        'location': location,
        'search_form': ItemSearchForm(initial={'item_name': item_name, 'location': location}),
        'results': results,
        'total_results': len(results)
    }
    
    return render(request, 'item_search_results.html', context)

@login_required
def edit_business(request, business_type, business_id):
    retailer = get_object_or_404(Retailer, user=request.user)
    
    # Get the business object based on type and ID
    business = None
    if business_type == 'restaurant':
        business = get_object_or_404(Restaurant, id=business_id, retailer=retailer)
    elif business_type == 'hotel':
        business = get_object_or_404(Hotel, id=business_id, retailer=retailer)
    elif business_type == 'gym':
        business = get_object_or_404(Gym, id=business_id, retailer=retailer)
    elif business_type == 'hospital':
        business = get_object_or_404(Hospital, id=business_id, retailer=retailer)
    elif business_type == 'retail':
        business = get_object_or_404(RetailStore, id=business_id, retailer=retailer)
    
    if not business:
        messages.error(request, "Business not found.")
        return redirect('retailer')
    
    if request.method == 'POST':
        # Update business fields
        business.name = request.POST.get('name')
        business.address = request.POST.get('location')
        business.phone = request.POST.get('contact') if business_type != 'retail' else business.phone
        
        if hasattr(business, 'description'):
            business.description = request.POST.get('description')
        
        # Type-specific fields
        if business_type == 'restaurant':
            business.cuisine_type = request.POST.get('cuisine_type', '')
            business.price_range = request.POST.get('price_range', '')
            business.opening_hours = request.POST.get('opening_hours', '')
        elif business_type == 'hotel':
            business.amenities = request.POST.get('amenities', '')
            business.price_range = request.POST.get('price_range', '')
        elif business_type == 'gym':
            business.facilities = request.POST.get('facilities', '')
            business.opening_hours = request.POST.get('opening_hours', '')
        elif business_type == 'retail':
            business.store_type = request.POST.get('store_type', '')
            business.operating_hours = request.POST.get('operating_hours', '')
        elif business_type == 'hospital':
            business.specialties = request.POST.get('specialties', '')
            business.emergency_services = request.POST.get('emergency_services') == 'Yes'
        
        business.save()
        messages.success(request, f"{business_type.capitalize()} updated successfully!")
        return redirect('retailer')
    
    return redirect('retailer')

# @login_required
# def get_business_details(request, business_type, business_id):
#     """API endpoint to get business details for the edit form"""
#     from django.http import JsonResponse
    
#     retailer = get_object_or_404(Retailer, user=request.user)
    
#     try:
#         data = {}
#         if business_type == 'restaurant':
#             business = get_object_or_404(Restaurant, id=business_id, retailer=retailer)
#             data = {
#                 'name': business.name,
#                 'location': business.address,
#                 'contact': business.phone,
#                 'description': business.description,
#                 'cuisine_type': business.cuisine_type,
#                 'price_range': business.price_range,
#                 'opening_hours': business.opening_hours
#             }
#         elif business_type == 'hotel':
#             business = get_object_or_404(Hotel, id=business_id, retailer=retailer)
#             data = {
#                 'name': business.name,
#                 'location': business.address,
#                 'contact': business.phone,
#                 'description': business.description,
#                 'amenities': business.amenities,
#                 'price_range': business.price_range
#             }
#         # Add similar blocks for other business types
        
#         return JsonResponse(data)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)


#debug pannel for retailer info
@login_required
def retailer_debug(request):
    """Debug view to inspect retailer object"""
    current_user = request.user
    retailer = get_object_or_404(Retailer, user=current_user)
    
    print("Retailer object:", retailer)
    print("Retailer type:", type(retailer))
    print("Retailer dir:", dir(retailer))
    
    # Get all field names
    field_names = [field.name for field in retailer._meta.fields]
    
    # Create a dict of field name -> value
    field_values = {}
    for name in field_names:
        field_values[name] = getattr(retailer, name, None)
    
    context = {
        'retailer': retailer,
        'field_names': field_names,
        'field_values': field_values,
    }
    
    return render(request, 'retailer/retailer_debug.html', context)


def interaction():
    pass