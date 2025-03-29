from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Restaurant
from .forms import SignupForm, CustomLoginForm 


def categoriesnew(request):
    return render(request, 'categoriesnew.html')

def contactus(request):
    return render(request, 'contactus.html')

def hotel(request):
    return render(request, 'hotel.html')

def newrestaurant(request):
    return render(request, 'newrestaurant.html')

def newretail(request):
    return render(request, 'newretail.html')

def newgym(request):
    return render(request, 'newgym.html')

def newhospital(request):
    return render(request, 'newhospital.html')

def profile(request):
    return render(request, '#')

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after signup
            return redirect("dashboard")  # Redirect to dashboard after signup
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')  # Can be username, email, or phone
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('user')  # Redirect to user dashboard

    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

def dashboard(request):
    if request.user.is_authenticated:
        return redirect('user')  # Redirect to user dashboard if logged in
    return render(request, 'index.html')  # Show homepage if not logged in

@login_required
def user_view(request):
    return render(request, 'user.html', {'user': request.user})  # Pass logged-in user

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

def profile(request):
    return render(request, 'profile.html', {'user': request.user})
