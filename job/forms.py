from django import forms
from django.contrib.auth import get_user_model

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
