from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.conf import settings

# Create your views here.

class CourseView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL
    
    def get(self,request):
        return render(request, 'course.html')
    