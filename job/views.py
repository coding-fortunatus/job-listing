# from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render  # redirect
from .forms import CustomUserRegistrationForm, CustomUserLoginForm


def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            print('Welcome to Job Listing')  # Redirect to homepage
    else:
        form = CustomUserRegistrationForm()
    return render(request, template_name='site/register.html', context={'form': form})


def user_login(request):
    if request.method == "POST":
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            print("Authenticated")  # Redirect to a user dashboard
    else:
        form = CustomUserLoginForm()

    return render(request, "site/login.html", {"form": form})
