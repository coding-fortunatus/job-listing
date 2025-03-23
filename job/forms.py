from django import forms
from django.contrib.auth import get_user_model
from .models import Job

User = get_user_model()


class CustomUserRegistrationForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'user@mail.example', 'class': 'form-control', 'autofill': 'off'}))
    fullname = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'John Doe', 'class': 'form-control', 'autofill': 'off'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(
        attrs={'placeholder': '+2348169418576', 'class': 'form-control', 'autofill': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autofill': 'off'}), required=True)
    role = forms.ChoiceField(
        choices=[('employer', 'Employer'), ('candidate', 'Candidate')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", 'autofill': 'off'}), required=True)

    def clean_email(self):
        """Ensure the email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_confirm_password(self):
        """Ensure passwords match"""
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password

    def save(self):
        email = self.cleaned_data['email']
        fullname = self.cleaned_data['fullname']
        phone = self.cleaned_data['phone']
        role = self.cleaned_data['role']
        password = self.cleaned_data['password']

        user = User.objects.create_user(
            email=email, fullname=fullname, phone=phone, role=role, password=password)
        return user


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = User  # Use your actual User model
        fields = [
            'fullname', 'position', 'phone',
            'picture', 'category', 'secondary_category', 'country_of_residence',
            'city_of_residence', 'salary_expectation', 'resume_cv', 'skills',
            'experience', 'english_level', 'work_experience', 'accomplishments',
            'expectations', 'employment_options'
        ]
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'category': forms.Select(attrs={'class': 'category'}),
            'secondary_category': forms.Select(attrs={'class': 'category'}),
            'country_of_residence': forms.TextInput(attrs={'class': 'form-control'}),
            'city_of_residence': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_expectation': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'resume_cv': forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'skills': forms.Textarea(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'english_level': forms.TextInput(attrs={'class': 'form-control'}),
            'work_experience': forms.Textarea(attrs={'class': 'form-control description-area'}),
            'accomplishments': forms.Textarea(attrs={'class': 'form-control description-area'}),
            'expectations': forms.Textarea(attrs={'class': 'form-control description-area'}),
            'employment_options': forms.Select(attrs={'class': 'form-control'}),
        }


class PostJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'job_category', 'company_name', 'company_email', 'company_website', 'location', 'job_type', 'job_tags', 'salary', 'experience',
            'description',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'job_category': forms.Select(attrs={'class': 'category'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company_website': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'category'}),
            'job_tags': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control description-area'}),
        }
