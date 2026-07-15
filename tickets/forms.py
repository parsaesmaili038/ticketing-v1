# tickets/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Ticket

class TicketForm(forms.ModelForm):
    # فیلد اضافی برای ارسال ناشناس
    anonymous = forms.BooleanField(
        required=False,
        label=_("ارسال به صورت ناشناس"),
        help_text=_("اگر این گزینه را فعال کنید، نام شما نمایش داده نخواهد شد.")
    )

    class Meta:
        model = Ticket
        # فیلدهایی از مدل Ticket که کاربر باید ببیند و تکمیل کند.
        fields = ['title', 'message'] # فقط عنوان و پیام

    def __init__(self, *args, **kwargs):
        """
        تنظیمات ظاهری فیلدها، مانند کلاس‌های Bootstrap.
        """
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control mb-2'})
        self.fields['message'].widget.attrs.update({'class': 'form-control mb-2', 'rows': 5})

    # متد save فرم را حذف می‌کنیم، چون مدیریت user و is_anonymous را به view منتقل می‌کنیم.
    # def save(self, commit=True): ...
