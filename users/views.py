from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import *
import re
from django.db import transaction
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def home(request):
    if request.user.type == 'teacher':
        return redirect('dashboard')
    elif request.user.type == 'student':
        return redirect('counter')
    

class Login(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #messages.success(request, _('Tizimga muvaffaqiyatli kirdingiz!'))
            if user.type == 'teacher':
                return redirect('dashboard') 
            elif user.type == 'student':
                return redirect('counter') 
        else:
            messages.error(request, _('Login yoki parol noto\'g\'ri.'))
            return render(request, 'login.html')
    

class Logout(View):
    def get(self, request):
        logout(request)
        messages.error(request, _('Tizimdan chiqdingiz.'))
        return redirect('login')




class SignUpTeacher(UserPassesTestMixin,View):
    def get(self,request):
        return render(request, 'sign_up_teacher.html')

    def test_func(self):
        return self.request.user.is_admin

    def post(self,request):
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        address = request.POST.get('address')
        work_place = request.POST.get('work_place')
        phone_number = request.POST.get('phone_number')

        # Validatsiyalar
        errors = []

        # Ism, sharif, familiya bo‘sh bo‘lmasligi kerak
        if not first_name or len(first_name) > 16:
            errors.append(_("Ism 16 ta belgidan oshmasligi kerak."))
        if not middle_name or len(middle_name) > 16:
            errors.append(_("Sharif 16 ta belgidan oshmasligi kerak."))
        if not last_name or len(last_name) > 16:
            errors.append(_("Familiya 16 ta belgidan oshmasligi kerak."))

        # Username uzunligi va mavjudligini tekshirish
        if not username or len(username) > 32 or len(username) < 3:
            errors.append(_("Foydalanuvchi nomi 3 tadan 32 ta belgigacha bo'lishi kerak."))
        if User.objects.filter(username=username).exists():
            errors.append(_("Bu foydalanuvchi nomi allaqachon mavjud."))

        # Parol validatsiyasi
        if not re.match(r'^[A-Za-z0-9]{8,16}$', password):
            errors.append(_("Parolda faqat 8-16 ta harf va raqam bo‘lishi kerak."))
        if password != password_confirmation:
            errors.append(_("Parol va tasdiqlash paroli bir xil emas."))

        # Manzil va ish joyi validatsiyasi
        if not address or len(address) > 100:
            errors.append(_("Manzil 100 ta belgidan oshmasligi kerak."))
        if not work_place or len(work_place) > 100:
            errors.append(_("Ish joyi 100 ta belgidan oshmasligi kerak."))

        # Telefon raqamni tekshirish
        if not phone_number.startswith('+998') or len(phone_number) != 13 or not phone_number[1:].isdigit():
            errors.append(_("Telefon raqam +998 bilan boshlanib, 13 ta belgidan iborat bo‘lishi kerak."))
        if Teacher.objects.filter(phone_number=phone_number).exists():
            errors.append(_("Bu telefon raqam allaqachon mavjud."))


        # Agar xatoliklar bo‘lsa, ularni foydalanuvchiga ko‘rsatish
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'sign_up_teacher.html', request.POST)

        # Ma'lumotlarni saqlash
        try:
            with transaction.atomic():
                user = User.objects.create(
                    first_name=first_name,
                    middle_name = middle_name,
                    type = 'teacher',
                    last_name=last_name,
                    username=username,
                    password=make_password(password)
                )
                teacher = Teacher.objects.create(
                    user=user,
                    address=address,
                    work_place=work_place,
                    phone_number=phone_number
                )
            return redirect('login')
        except Exception as e:
            messages.error(request, _(f"Xatolik yuz berdi: {str(e)}"))
            return render(request, 'sign_up_teacher.html', request.POST)


class SignUpStudent(View):
    def get(self, request):
        return render(request, 'sign_up_student.html')

    def post(self,request):
    # POST'dan ma'lumotlarni olish
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        school = request.POST.get('school')
        faculty = request.POST.get('faculty')
        group = request.POST.get('group')
        birth_date = request.POST.get('birth_date')
        experience = request.POST.get('experience')
        email = request.POST.get('email')
        telegram = request.POST.get('telegram')
        phone_number = request.POST.get('phone_number')

        # Validatsiyalar
        errors = []

        # Ism, sharif, familiya bo‘sh bo‘lmasligi kerak
        if not first_name or len(first_name) > 16:
            errors.append(_("Ism 16 ta belgidan oshmasligi kerak."))
        if not middle_name or len(middle_name) > 16:
            errors.append(_("Sharif 16 ta belgidan oshmasligi kerak."))
        if not last_name or len(last_name) > 16:
            errors.append(_("Familiya 16 ta belgidan oshmasligi kerak."))

        # Username uzunligi va mavjudligini tekshirish
        if not username or len(username) > 32 or len(username) < 3:
            errors.append(_("Foydalanuvchi nomi 3 tadan 32 ta belgigacha bo'lishi kerak."))
        if User.objects.filter(username=username).exists():
            errors.append(_("Bu foydalanuvchi nomi allaqachon mavjud."))

        # email uzunligi va mavjudligini tekshirish
        if not email or len(email) > 100 or len(email) < 10:
            errors.append(_("Elektron pochta 10 tadan 100 ta belgigacha bo'lishi kerak."))
        if Student.objects.filter(email=email).exists():
            errors.append(_("Bu Elektron pochta allaqachon mavjud."))
        if not re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email):
            errors.append(_("Elektron pochta formati noto'g'ri"))

        # Parol validatsiyasi
        if not re.match(r'^[A-Za-z0-9]{8,16}$', password):
            errors.append(_("Parolda faqat 8-16 ta harf va raqam bo‘lishi kerak."))
        if password != password_confirmation:
            errors.append(_("Parol va tasdiqlash paroli bir xil emas."))

        # Manzil va ish joyi validatsiyasi
        if not school or len(school) > 100:
            errors.append(_("O'qish joyi 100 ta belgidan oshmasligi kerak."))
        if not faculty or len(faculty) > 100:
            errors.append(_("Fakultet 100 ta belgidan oshmasligi kerak."))
        if not group or len(group) > 100:
            errors.append(_("Guruh 100 ta belgidan oshmasligi kerak."))

        # Telefon raqamni tekshirish
        if not phone_number.startswith('+998') or len(phone_number) != 13 or not phone_number[1:].isdigit():
            errors.append(_("Telefon raqam +998 bilan boshlanib, 13 ta belgidan iborat bo‘lishi kerak."))
        if Teacher.objects.filter(phone_number=phone_number).exists():
            errors.append(_("Bu telefon raqam allaqachon mavjud."))

        # Agar xatoliklar bo‘lsa, ularni foydalanuvchiga ko‘rsatish
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'sign_up_student.html', request.POST)

        # Ma'lumotlarni saqlash
        try:
            with transaction.atomic():
                user = User.objects.create(
                    first_name=first_name,
                    middle_name = middle_name,
                    type = 'student',
                    last_name=last_name,
                    username=username,
                    password=make_password(password)
                )
                student = Student.objects.create(
                    user=user,
                    school=school,
                    phone_number=phone_number,
                    faculty=faculty,
                    group=group,
                    birth_date=birth_date,
                    experience=experience,
                    email=email,
                    telegram=telegram
                )
            return redirect('login')
        except Exception as e:
            messages.error(request, _(f"Xatolik yuz berdi: {str(e)}"))
            return render(request, 'sign_up_student.html', request.POST)








        