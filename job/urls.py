from django.urls import path
from .views import register, user_login, index, user_logout, profile, post_job, job_details, recommended_jobs, apply, user_applied_jobs

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('profile', profile, name='profile'),
    path('post-job', post_job, name="post_job"),
    path('recommended-jobs', recommended_jobs, name='recommended_jobs'),
    path('job/<int:job_id>', job_details, name='job_details'),
    path('job/<int:job_id>/apply', apply, name='apply'),
    path('user-applied-jobs', user_applied_jobs, name='user_applied_jobs')
]
