# tickets/models.py

from django.db import models
from django.conf import settings # برای دسترسی به User model اصلی
from django.utils.translation import gettext_lazy as _ # برای چندزبانه کردن (اختیاری)
from django.contrib.auth import get_user_model

User = get_user_model()

class Ticket(models.Model):
    # --- اصلاح شده ---
    # نام فیلد درست شد: user
    # و از settings.AUTH_USER_MODEL استفاده شد که بهتره
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # استفاده از SET_NULL به جای CASCADE بهتره چون تیکت پاک نشه
        null=True,
        blank=True,
        related_name='tickets',
        verbose_name=_("کاربر")
    )
    # فیلد is_anonymous فقط یک بار تعریف شود
    is_anonymous = models.BooleanField(default=False, verbose_name=_("ناشناس ثبت شده؟"))
    # --- پایان اصلاح ---

    title = models.CharField(max_length=200, verbose_name=_("عنوان تیکت"))
    message = models.TextField(blank=True, null=True) # می‌تونه خالی باشه

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("زمان ثبت"))
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', _('جدید')),
            ('open', _('در حال بررسی')),
            ('closed', _('بسته شده')),
        ],
        default='new',
        verbose_name=_("وضعیت")
    )

    def __str__(self):
        if self.user:
            return f"{_('Ticket')} {self.id} {_('from')} {self.user.username} ({self.title})"
        else:
            return f"{_('Anonymous Ticket')} {self.id} ({self.title})"

    class Meta:
        verbose_name = _("تیکت")
        verbose_name_plural = _("تیکت‌ها")
        ordering = ['-created_at'] # نمایش تیکت‌های جدیدتر اول
