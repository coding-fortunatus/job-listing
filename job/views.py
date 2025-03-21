# from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import CustomUserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Job

User = get_user_model()


def index(request):
    jobs = Job.objects.all()
    return render(request, 'site/index.html', {'jobs': jobs})


def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            redirect('login')  # Redirect to homepage
    else:
        form = CustomUserRegistrationForm()
    return render(request, template_name='site/register.html', context={'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "").strip()

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return redirect("login")

        # Check if user exists before authenticating
        if not User.objects.filter(email=email).exists():
            messages.error(request, "Invalid email or password.")
            return redirect("login")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")

        messages.error(request, "Invalid email or password.")
        return redirect("login")

    return render(request, template_name="site/login.html")


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')
