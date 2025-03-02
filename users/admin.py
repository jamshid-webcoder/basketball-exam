from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class StudentInline(admin.StackedInline):  
    model = Student

class TeacherInline(admin.StackedInline): 
    model = Teacher

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'middle_name', 'last_name', 'type',)
    list_filter = ('type', 'is_active')
    search_fields = ('username', 'first_name', 'middle_name', 'last_name',)
    ordering = ('-id',)
    inlines = (StudentInline, TeacherInline,)


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'middle_name', 'last_name', 'type', 'password1', 'password2', 'is_active', 'is_admin'),
        }),
    )


    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Shaxsiy maʼlumotlar', {'fields': ('first_name', 'middle_name', 'last_name','type')}),
        ('Foydalanuvchi holati', {'fields': ('is_active', 'is_admin')}),
        
    )

    readonly_fields = ('date_joined', 'last_login',)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Teacher)
admin.site.register(Student)