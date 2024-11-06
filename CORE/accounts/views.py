from django.shortcuts import render, redirect
from .forms import SignUpForm, UserLoginForm, ProfileForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
import logging

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('profile_edit')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):  # Renamed to avoid collision
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirect to a home or profile page after login
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {'form': form})

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'profile_view.html', {'profile': profile})

logger = logging.getLogger(__name__)
@login_required
def user_logout(request):
    username = request.user.username
    logout(request)
    logger.debug(f"User {username} has logged out.")
    return redirect('home')