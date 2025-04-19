from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from .models import Restaurant, Hotel, Gym, Hospital, RetailStore, Review, Contact, Category, CustomUser, MenuItem, \
    UserChat
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
def add_review(request, business_id=None):
    # First, try to find the business and its type
    business = None
    business_type = None

    # Check each business type
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

    if not business or not business_type:
        messages.error(request, 'Business not found')
        return redirect('index')

    if request.method == 'POST':
        try:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')

            # Validate inputs
            if not all([rating, comment]):
                raise ValidationError('All fields are required')

            try:
                rating = int(rating)
                if not 1 <= rating <= 5:
                    raise ValidationError('Rating must be between 1 and 5')
            except ValueError:
                raise ValidationError('Invalid rating value')

            # Create the review
            review = Review.objects.create(
                user=request.user,
                business_type=business_type,
                business_id=business_id,
                rating=rating,
                comment=comment
            )

            messages.success(request, 'Review added successfully!')
            return redirect(business_type)

        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            print(f"Error in add_review: {str(e)}")  # For debugging
            messages.error(request, 'Error adding review. Please try again.')

    # For GET requests or if there's an error in POST
    context = {
        'business': business,
        'business_id': business_id,
        'business_type': business_type
    }
    return render(request, 'add_review.html', context)


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


from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import UserChat, User
import json

@login_required
def chat(request):
    user = request.user

    # Get all unique chat partners
    partner_ids = set()
    # Partners who sent messages to current user
    partner_ids.update(UserChat.objects.filter(sent_to=user).values_list('user_id', flat=True))
    # Partners who received messages from current user
    partner_ids.update(UserChat.objects.filter(user=user).values_list('sent_to_id', flat=True))

    partners = CustomUser.objects.filter(id__in=partner_ids)

    # Get selected partner from query parameter
    selected_partner_id = request.GET.get('partner')
    selected_partner = None
    chats = []

    if selected_partner_id:
        try:
            selected_partner = CustomUser.objects.get(id=selected_partner_id)
            # Get messages between current user and selected partner
            chats = UserChat.objects.filter(
                (Q(user=user) & Q(sent_to=selected_partner)) |
                (Q(user=selected_partner) & Q(sent_to=user))
            ).order_by('created_at')
        except User.DoesNotExist:
            pass

    context = {
        'partners': partners,
        'chats': chats,
        'selected_partner': selected_partner,
    }
    return render(request, 'chat.html', context)

@login_required
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message_text = data.get('message')
            sent_to_id = data.get('sent_to')

            receiver = CustomUser.objects.get(id=sent_to_id)
            new_chat = UserChat.objects.create(
                user=request.user,
                sent_to=receiver,
                message=message_text,
                status=0
            )
            return JsonResponse({
                'status': 'success',
                'message': {
                    'id': new_chat.id,
                    'text': new_chat.message,
                    'sender': request.user.username,
                    'timestamp': new_chat.created_at.strftime('%b %d, %Y, %I:%M %p'),
                    'is_sender': True,
                    'status': new_chat.status
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def get_partner_chats(request, partner_id):
    try:
        partner = CustomUser.objects.get(id=partner_id)
        chats = UserChat.objects.filter(
            (Q(user=request.user) & Q(sent_to=partner)) |
            (Q(user=partner) & Q(sent_to=request.user))
        ).order_by('created_at')

        # Mark received messages as read
        UserChat.objects.filter(user=partner, sent_to=request.user, status=0).update(status=1)

        chats_data = [{
            'id': chat.id,
            'text': chat.message,
            'sender': chat.user.username,
            'timestamp': chat.created_at.strftime('%b %d, %Y, %I:%M %p'),
            'is_sender': chat.user == request.user,
            'status': chat.status
        } for chat in chats]

        return JsonResponse({
            'status': 'success',
            'chats': chats_data,
            'partner_name': partner.username
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})