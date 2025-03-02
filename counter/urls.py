from django.urls import path
from .views import *

urlpatterns = [
    path('', Counter.as_view(), name='counter'),
     path('correct_attempts/', CorrectAttemptView.as_view(), name='correct_attempts'),
    path('result/', Result.as_view(), name='result'),
]
