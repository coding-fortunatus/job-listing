from django.urls import path
from .views import register, user_login, index, user_logout, profile, post_job

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('post-job/', post_job, name="post_job"),
]
