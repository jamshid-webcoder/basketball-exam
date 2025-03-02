from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Attempt(models.Model):

    TYPE_ATTEMPTS = [
        ('penalty', _('Jarima zarbasi')),
        ('average', _('O\'rta zarba')),
        ('further', _('Uzoq masofali zarba')),
    ]

    POSITION_SHOOT = [
        ('center', _('Markaziy')),
        ('right/45', _('O\'ng / 45\'')),
        ('right/90', _('O\'ng / 90\'')),
        ('left/45', _('Chap / 45\'')),
        ('left/90', _('Chap / 90\'')),
    ]

    student = models.ForeignKey('users.Student', verbose_name=_('Talaba'), on_delete=models.CASCADE, blank=False, null=False)
    type = models.CharField(verbose_name=_('Zarba turi'),choices=TYPE_ATTEMPTS , max_length=100, blank=False, null=False)
    position = models.CharField(verbose_name=_('Otish holati'),choices=POSITION_SHOOT ,max_length=100, null=True, blank=True)
    attempts = models.IntegerField(verbose_name=_('Urinishlar'), blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def type_attempt_display(self):
        return dict(self.TYPE_ATTEMPTS).get(self.type, self.type)

    @property
    def position_shoot_display(self):
        return dict(self.POSITION_SHOOT).get(self.position, self.position)

    class Meta:
        verbose_name = _("Urinish")
        verbose_name_plural = _("Urinishlar")

    def __str__(self):
        return f"attempt {self.student.user.username} {self.id}"
    

class CorrectAttempt(models.Model):
    attempt = models.ForeignKey("counter.Attempt", verbose_name=_("Urinish"), on_delete=models.CASCADE,blank=False, null=False, related_name="correct_attempts")
    is_succesfull = models.BooleanField(_("To'g'ri urinish"), default=True)


    class Meta:
        verbose_name = _("To'g'ri urinish")
        verbose_name_plural = _("To'g'ri urinishlar")

    def __str__(self):
        return f"correct attempt {self.attempt.student.user.username} {self.attempt.id}"

