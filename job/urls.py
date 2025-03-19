from django.urls import path
from .views import register, user_login

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
]
