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
    position = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Senior Software Engineer', 'class': 'form-control', 'autofill': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autofill': 'off'}), required=True)
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
        position = self.cleaned_data['position']
        password = self.cleaned_data['password']

        user = User.objects.create_user(
            email=email, fullname=fullname, phone=phone, position=position, password=password)
        return user


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = User  # Use your actual User model
        fields = [
            'picture', 'category', 'secondary_category', 'country_of_residence',
            'city_of_residence', 'salary_expectation', 'resume_cv', 'skills',
            'experience', 'english_level', 'work_experience', 'accomplishments',
            'expectations', 'employment_options'
        ]
        widgets = {
            'picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'secondary_category': forms.Select(attrs={'class': 'form-control'}),
            'country_of_residence': forms.TextInput(attrs={'class': 'form-control'}),
            'city_of_residence': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_expectation': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'resume_cv': forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'skills': forms.Textarea(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'english_level': forms.TextInput(attrs={'class': 'form-control'}),
            'work_experience': forms.Textarea(attrs={'class': 'form-control'}),
            'accomplishments': forms.Textarea(attrs={'class': 'form-control'}),
            'expectations': forms.Textarea(attrs={'class': 'form-control'}),
            'employment_options': forms.Select(attrs={'class': 'form-control'}),
        }


class PostJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'job_type', 'location',
            'company', 'salary',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.TextInput(attrs={'class': 'form-control'}),
        }
