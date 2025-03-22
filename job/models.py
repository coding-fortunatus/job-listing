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
    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    ]
    EMPLOYMENT_OPTIONS = [
        ('', 'Select Employment Type'),
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('volunteer', 'Volunteer')
    ]
    CATEGORY_CHOICES = [
        ('', 'Select Category'),
        ('software_development', 'Software Development'),
        ('design', 'Design'),
        ('human_resources', 'Human Resources'),
        ('education', 'Education'),
        ('engineering', 'Engineering'),
        ('data_science', 'Data Science'),
        ('cybersecurity', 'Cybersecurity'),
        ('blockchain', 'Blockchain'),
        ('gaming', 'Gaming'),
        ('AI_ML', 'AI & Machine Learning'),
        ('telecommunications', 'Telecommunications'),
        ('other', 'Other')
    ]
    username = None  # Remove username field
    first_name = None  # Ignore first_name
    last_name = None  # Ignore last_name
    # Database user fields definitions
    email = models.EmailField(unique=True)  # Ensure email is unique
    fullname = models.CharField(max_length=255)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='job_seeker')
    phone = models.CharField(max_length=15, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    category = models.CharField(
        max_length=255, blank=True, null=True, choices=CATEGORY_CHOICES)
    secondary_category = models.CharField(
        max_length=255, blank=True, null=True, choices=CATEGORY_CHOICES)
    country_of_residence = models.CharField(
        max_length=255, blank=True, null=True)
    city_of_residence = models.CharField(max_length=255, blank=True, null=True)
    salary_expectation = models.IntegerField(blank=True, null=True)
    resume_cv = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    experience = models.IntegerField(
        blank=True, null=True)
    english_level = models.CharField(
        max_length=100, blank=True, null=True)
    work_experience = models.TextField(blank=True, null=True)
    accomplishments = models.TextField(blank=True, null=True)
    expectations = models.TextField(blank=True, null=True)
    employment_options = models.CharField(
        max_length=20, choices=EMPLOYMENT_OPTIONS, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()  # Use custom manager

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['fullname', 'phone']  # required fields

    def __str__(self):
        return self.fullname


class Job(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    job_category = models.CharField(
        max_length=255, choices=User.CATEGORY_CHOICES, null=True, blank=True)
    job_type = models.CharField(
        choices=User.EMPLOYMENT_OPTIONS, max_length=20)
    job_tags = models.CharField(max_length=255)
    experience = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_email = models.EmailField(max_length=255, null=True, blank=True)
    company_website = models.URLField(max_length=255, blank=True, null=True)
    salary = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title, ":", self.company_name
