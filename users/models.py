from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self,first_name, middle_name, last_name, username, type, password=None, **extra_fields):
        if not first_name:
            raise ValueError(_('Ism kiritilishi kerak'))
        if not last_name:
            raise ValueError(_('Familiya kiritilishi kerak'))
        if not username:
            raise ValueError(_('Foydalanuvchi nomi kiritilishi kerak'))
        if not type:
            raise ValueError(_('Foydalanuvchi turi tanlanishi kerak'))
        
        user = self.model(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            username=username,
            type=type,
            **extra_fields
        )
        if password:
            user.password = make_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, middle_name, last_name, username, type='teacher', password=None, **extra_fields):
        user = self.create_user(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            username=username,
            type=type,
            password=password,
            **extra_fields
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class  User(AbstractBaseUser, PermissionsMixin):
    TYPE_CHOICES = [
        ('teacher', _('Murabbiy')),
        ('student', _('Talaba')),
    ]   

    first_name = models.CharField(max_length=30, verbose_name=_('Ism'))
    middle_name = models.CharField(max_length=30,verbose_name=_('Otasining ismi'))
    last_name = models.CharField(max_length=30, verbose_name='Familiya')
    username = models.CharField(max_length=30, unique=True, verbose_name=_('Foydalanuvchi nomi'))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('Ro‘yxatdan o‘tgan sana'))
    last_login = models.DateTimeField(auto_now=True, verbose_name=_('Oxirgi kirish vaqti'))
    is_active = models.BooleanField(default=True, verbose_name=_('Faol'))
    is_admin = models.BooleanField(default=False, verbose_name=_('Admin'))
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=False, blank=False, verbose_name=_('Foydalanuvchi turi'))

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name',]

    class Meta:
        verbose_name = _('Foydalanuvchi')
        verbose_name_plural = _('Foydalanuvchilar')

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Teacher(models.Model):
    user = models.OneToOneField("users.User", verbose_name=_("Foydalanuvchi"), on_delete=models.CASCADE, related_name='teacher')
    phone_number = models.CharField(max_length=15, unique=True, verbose_name=_('Telefon raqam'),help_text='+998*********')
    work_place = models.CharField(_("Ish joyi"), max_length=100)
    address = models.CharField(_("Manzil"), max_length=100)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Murabbiy')
        verbose_name_plural = _('Murabbiylar')

    
class Student(models.Model):
    user = models.OneToOneField("users.User", verbose_name=_("Foydalanuvchi"), on_delete=models.CASCADE, related_name='student')
    phone_number = models.CharField(max_length=15, unique=True, verbose_name=_('Telefon raqam'),help_text='+998*********')
    school = models.CharField(verbose_name="Ta'lim joyi", max_length=50, help_text='BuxDU')
    faculty = models.CharField(_("Fakultet"), max_length=50)
    group = models.CharField(_("Guruh"), max_length=50)
    birth_date = models.DateField(blank=False, null=False, verbose_name=_('Tug\'ilgan sana'))
    experience = models.PositiveSmallIntegerField(_("Basketboldagi tajribasi"))
    email = models.EmailField(_("Elektron pochta"), max_length=254, unique=True, help_text="example@gmail.com")
    telegram = models.URLField(_("Telegram manzili"), max_length=200, blank=True, null=True, help_text="https://telegram.me/username")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Talaba')
        verbose_name_plural = _('Talabalar')