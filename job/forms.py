from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserRegistrationForm(forms.Form):
    email = forms.EmailField(required=True)
    fullname = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=15, required=True)
    position = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self):
        email = self.cleaned_data['email']
        fullname = self.cleaned_data['fullname']
        phone = self.cleaned_data['phone']
        position = self.cleaned_data['position']
        password = self.cleaned_data['password']

        user = User.objects.create_user(
            email=email, fullname=fullname, phone=phone, position=position, password=password)
        return user


class CustomUserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()
            if user is None:
                raise forms.ValidationError("Invalid email or password")

            if not user.check_password(password):
                raise forms.ValidationError("Invalid email or password")
            cleaned_data['user'] = user
        return cleaned_data
