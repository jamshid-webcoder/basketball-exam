from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path('sign_up_teacher/', SignUpTeacher.as_view(), name="sign_up_teacher"),
    path('sign_up_student/', SignUpStudent.as_view(), name="sign_up_student"),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

]
