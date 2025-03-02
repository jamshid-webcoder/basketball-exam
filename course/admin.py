from django.contrib import admin
from .models import Lesson
from tinymce.widgets import TinyMCE
from django import forms

class LessonAdminForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Lesson
        fields = '__all__'

class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm

admin.site.register(Lesson, LessonAdmin)

