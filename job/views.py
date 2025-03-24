# from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import CustomUserRegistrationForm, UpdateUserProfileForm, PostJobForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Job

User = get_user_model()


# @login_required(login_url='login')
def index(request):
    if request.method == 'GET':
        title = request.GET.get('title')
        location = request.GET.get('location')
        if title and location:
            jobs = Job.objects.filter(
                title__icontains=title, location__icontains=location)
        elif title:
            jobs = Job.objects.filter(title__icontains=title)
        elif location:
            jobs = Job.objects.filter(location__icontains=location)
        else:
            jobs = Job.objects.all()
    return render(request, template_name='site/index.html', context={'jobs': jobs})


@login_required(login_url='login')
def recommended_jobs(request):
    jobs = Job.objects.filter(job_tags__icontains=request.user.category)
    return render(request, template_name='site/recommend.html', context={'jobs': jobs})


def job_details(request, job_id):
    job = Job.objects.get(id=job_id)
    tags = job.job_tags.split(',')
    requirements = [req.strip()
                    for req in job.requirements.split("\n") if req.strip()]
    return render(request, template_name='site/job-details.html', context={'job': job, 'tags': tags, 'requirements': requirements})


def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            redirect('index')  # Redirect to homepage
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


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        form = UpdateUserProfileForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('profile')
    else:
        form = UpdateUserProfileForm(instance=request.user)
    return render(request, template_name='site/profile.html', context={'form': form})


@login_required(login_url='login')
def post_job(request):
    if request.method == 'POST':
        form = PostJobForm(request.POST)
        form.instance.user_id = request.user
        if form.is_valid():
            form.save()
            messages.success(request, "Job posted successfully")
            return redirect('index')
    else:
        form = PostJobForm()
    return render(request, template_name='site/post-job.html', context={'form': form})
