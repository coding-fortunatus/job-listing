# from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import CustomUserRegistrationForm, UpdateUserProfileForm, PostJobForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Job, Application

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
        # Restrict users that are not employer from posting job advert
        if request.user.role != 'employer':
            messages.warning(request, "Candidate cannot post job advert")
            return redirect('index')
        form = PostJobForm(request.POST)
        form.instance.user_id = request.user
        if form.is_valid():
            form.save()
            messages.success(request, "Job posted successfully")
            return redirect('index')
    else:
        form = PostJobForm()
    return render(request, template_name='site/post-job.html', context={'form': form})


def job_details(request, job_id):
    job = Job.objects.get(id=job_id)
    tags = job.job_tags.split(',')
    requirements = [req.strip()
                    for req in job.requirements.split("\n") if req.strip()]
    return render(request, template_name='site/job-details.html', context={'job': job, 'tags': tags, 'requirements': requirements})


@login_required(login_url='login')
def recommended_jobs(request):
    jobs = Job.objects.filter(job_tags__icontains=request.user.category)
    return render(request, template_name='site/recommend.html', context={'jobs': jobs})


@login_required(login_url='login')
def user_applied_jobs(request):
    jobs = Application.objects.filter(user=request.user)
    return render(request, template_name='site/applied_jobs.html', context={'jobs': jobs})


@login_required(login_url='login')
def employer_jobs(request):
    jobs = Job.objects.filter(user_id=request.user)
    return render(request, template_name='site/employer-jobs.html', context={'jobs': jobs})


@login_required(login_url='login')
def apply(request, job_id):
    jobTo = Job.objects.get(id=job_id)
    userResume = request.user.resume_cv.name.replace('resumes/', '')

    if request.method == "POST":
        # Restrict employer or Job poster from applying to job
        if Job.objects.filter(id=job_id, user_id=request.user).exists() or request.user.role == 'employer':
            messages.warning(request, "Employer cannot apply for this job.")
            return redirect('job_details', job_id=job_id)

        # Check if the user has already applied
        if Application.objects.filter(user=request.user, job=jobTo).exists():
            messages.warning(request, "You have already applied for this job.")
            return redirect('job_details', job_id=job_id)

        # Get form data
        cover = request.POST.get('message', '').strip()
        resume = request.user.resume_cv
        user = request.user

        # Save the application
        Application.objects.create(
            user=user, job=jobTo, cover=cover, resume=resume)
        messages.success(request, "Application submitted successfully.")
        return redirect('job_details', job_id=job_id)
    return render(request, template_name='site/apply.html', context={'job': jobTo, 'resume': userResume})


def applications(request):
    applications = Application.objects.filter(job__user_id=request.user)
    return render(request, template_name='site/applications.html', context={'applications': applications})
