from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

# Create your models here.

class Lesson(models.Model):
    order = models.PositiveSmallIntegerField(_("Tartib raqam"), blank=False, null=False)
    title = models.CharField(_("Sarlavha"), max_length=150)
    body = HTMLField()

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Dars'
        verbose_name_plural = 'Darslar'