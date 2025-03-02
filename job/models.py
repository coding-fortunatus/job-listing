from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, fullname, password=None, **extra_fields):
        """Create and return a regular user with email and fullname required."""
        if not email:
            raise ValueError("The Email field must be set")
        if not fullname:
            raise ValueError("The Full Name field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, fullname, password, **extra_fields)


class User(AbstractUser):

    username = None  # Remove username field
    first_name = None  # Ignore first_name
    last_name = None  # Ignore last_name

    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    ]
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='job_seeker')
    phone = models.CharField(max_length=15, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    experience = models.IntegerField(
        blank=True, null=True, help_text="Years of experience")
    education = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)

    objects = CustomUserManager()  # Use custom manager

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['fullname']  # fullname is required


def __str__(self):
    return self.fullname
