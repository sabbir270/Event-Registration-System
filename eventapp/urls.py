from django.urls import path
from .views import home
urlpatterns = [
    path('',home),
    # Add other URL patterns as needed
]