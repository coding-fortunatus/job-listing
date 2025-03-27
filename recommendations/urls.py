from django.urls import path
from .views import recommendations

urlpatterns = [
    path('recommendations/<int:user_id>/',
         recommendations, name='recommendations'),
]
