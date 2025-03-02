from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

# Create your views here.

class Dashboard(LoginRequiredMixin,UserPassesTestMixin ,View):
    def get(self,request):
        return render(request, 'dashboard.html')
    def test_func(self):
        if self.request.user.type == 'teacher' or self.request.user.is_admin:
            return True