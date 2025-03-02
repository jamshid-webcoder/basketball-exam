from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Attempt, CorrectAttempt
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

class Counter(LoginRequiredMixin,UserPassesTestMixin,View):
    login_url=settings.LOGIN_URL

    def test_func(self):
        if self.request.user.type == 'student' or self.request.user.is_admin:
            return True

    def get(self,request):
        return render(request, 'counter.html')
    
    def post(self,request):
        type = request.POST.get('type')
        position = request.POST.get('position')
        attempts = request.POST.get('attempts') 

        errors = []

        if not (type  and attempts):
            errors.append(_("Barcha maydonlar to'ldirilishi kerak!"))

        if int(attempts) <= 0:
            errors.append(_("Jami urinishlar soni 0 dan katta bo'lishi kerak!"))

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'counter.html',)

        try:
            attempt = Attempt.objects.create(
                    student=self.request.user.student,
                    type = type,
                    position = position,
                    attempts=int(attempts),
                )
            return redirect('counter')
        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {e}")
            return redirect('counter')



@method_decorator(csrf_exempt, name='dispatch')
class CorrectAttemptView(View):
    # login_url=settings.LOGIN_URL

    # def test_func(self):
    #     return self.request.user.is_admin
    
    # def get(self,request):
    #     return HttpResponse("Signal qabul qilindi")

    def post(self,request): 
        API_KEY = "1qw23er45ty67ui89o"
        api_key = request.headers.get("API-KEY")
        
        if api_key != API_KEY: 
            return JsonResponse({"error": "Xatolik bor"}, status=403)


        attempt = Attempt.objects.all().last()
        
        CorrectAttempt.objects.create(attempt=attempt, is_succesfull=True)
        return HttpResponse("Signal qabul qilindi")



class Result(LoginRequiredMixin,UserPassesTestMixin,View):
    login_url=settings.LOGIN_URL
    
    def test_func(self):
        if self.request.user.type == 'student' or self.request.user.is_admin:
            return True

    def get(self,request):
        attempt = Attempt.objects.all().last()
        if request.user.type == 'student' and request.user.student != attempt.student:
            return HttpResponse(_("Iltimos natijani ko'rishdan oldin urinishlaringiz uchun ma'lumotlarni kiriting! "))
        if attempt:
            attempts = attempt.attempts
            correct_attempts = attempt.correct_attempts.count()
        
            if correct_attempts != 0:
                ratio = correct_attempts/attempts*100
            else:
                ratio = 0

            if correct_attempts > attempts:
                return HttpResponse(_('Sizning to\'g\'ri urinishlaringiz soni jami urinishlaringizning sonidan katta! Natijangiz 100%'))
            
            ctx = {
                'attempt' : attempt,
                'attempts':attempts,
                'correct_attempts': correct_attempts,
                'ratio': ratio
            }
        else:
            ctx = {}
        return render(request, 'result.html', ctx)
    

        