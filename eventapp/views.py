from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from .forms import UserRegistrationForm
from .forms import UserLoginForm


def home(request):
    return render(request,'eventapp/home.html')

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('eventapp:home')  
    else:
        form = UserRegistrationForm()

    return render(request, 'eventapp/user_registration.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('eventapp:home')


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('eventapp:home') 
    else:
        form = UserLoginForm()

    return render(request, 'eventapp/login.html', {'form': form})

