from django.urls import path
from .views import *

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard')
]
