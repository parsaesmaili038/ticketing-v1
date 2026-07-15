from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import hashlib
import uuid # اگر بخواهیم از UUID استفاده کنیم

# --- شبیه‌سازی مدل (اگر نمی‌خواهید مدل اصلی را تغییر دهید) ---
# اگر بتوانید مدل اصلی Ticket را تغییر دهید، این قسمت لازم نیست.
# ولی برای "یک فایل بودن" شبیه‌سازی می‌کنیم.

class AnonymousTicketData:
    def __init__(self, user_id, title, description, created_at, is_anonymous=False, anonymous_id=None):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.created_at = created_at
        self.is_anonymous = is_anonymous
        self.anonymous_id = anonymous_id if anonymous_id else str(uuid.uuid4())[:8] # یک شناسه کوتاه
        self.user = User.objects.get(id=user_id) if User.objects.filter(id=user_id).exists() else None # برای نمایش اسم

    def display_name(self):
        return "کاربر ناشناس" if self.is_anonymous else (self.user.username if self.user else "کاربر حذف شده")

    # برای اینکه بتوانیم از این کلاس در لیست تمپلیت استفاده کنیم
    @property
    def anonymous_hash(self):
        # هش واقعی را اینجا هم می‌توان تولید کرد اگر نیاز بود
        return self.anonymous_id # فعلا از شناسه کوتاه استفاده می‌کنیم

# --- شبیه‌سازی دیتابیس (فقط برای مثال) ---
# در پروژه واقعی، اینها از دیتابیس واقعی گرفته می‌شوند.
# ما اینجا از یک لیست برای نگهداری موقت استفاده می‌کنیم
MOCK_TICKETS_DB = []
from datetime import datetime

def add_mock_ticket(user_id, title, description, is_anonymous=False):
    new_ticket = AnonymousTicketData(
        user_id=user_id,
        title=title,
        description=description,
        created_at=datetime.now(),
        is_anonymous=is_anonymous,
    )
    MOCK_TICKETS_DB.append(new_ticket)
    return new_ticket

def get_all_mock_tickets():
    return sorted(MOCK_TICKETS_DB, key=lambda x: x.created_at, reverse=True)

# --- فرم برای ایجاد تیکت ---
class AnonymousTicketForm(forms.Form):
    title = forms.CharField(max_length=200, label="عنوان تیکت")
    description = forms.CharField(widget=forms.Textarea, label="توضیحات")
    is_anonymous = forms.BooleanField(required=False, label="ثبت به صورت ناشناس")

    # اگر کاربر لاگین نباشد، این فیلد اضافه شود
    # anonymous_name = forms.CharField(max_length=100, required=False, label="نام مستعار (اختیاری)")

# --- ویو برای ایجاد تیکت ---
def anonymous_ticket_create_view(request):
    if request.method == 'POST':
        form = AnonymousTicketForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            is_anonymous = form.cleaned_data['is_anonymous']

            user_id = request.user.id if request.user.is_authenticated else None

            if user_id is None and not is_anonymous:
                # اگر کاربر لاگین نیست و ناشناس هم نمی‌خواهد باشد، باید یک نام وارد کند
                # یا اینکه اجبار کنیم که یا لاگین باشد یا ناشناس
                # فعلا خطا می‌دهیم:
                return render(request, 'tickets/anonymous_ticket_form.html', {
                    'form': form,
                    'error': "برای ثبت تیکت لطفا وارد حساب کاربری خود شوید یا تیکت را به صورت ناشناس ثبت کنید."
                })
            
            # اگر کاربر ناشناس است، شناسه کاربری واقعی را null می‌گذاریم
            # و شناسه ناشناس را تولید می‌کنیم.
            ticket = add_mock_ticket(
                user_id=user_id,
                title=title,
                description=description,
                is_anonymous=is_anonymous
            )
            
            # در پروژه واقعی، اینجا ticket.save() را صدا می‌زنید
            
            return redirect(reverse('anonymous_ticket_list')) # هدایت به لیست تیکت‌ها
    else:
        form = AnonymousTicketForm()
        
    return render(request, 'tickets/anonymous_ticket_form.html', {'form': form})

# --- ویو برای نمایش لیست تیکت‌ها ---
def anonymous_ticket_list_view(request):
    # در پروژه واقعی، تیکت‌ها را از دیتابیس می‌گیرید
    # tickets = Ticket.objects.all().order_by('-created_at')
    tickets = get_all_mock_tickets() # استفاده از داده‌های شبیه‌سازی شده
    
    return render(request, 'tickets/anonymous_ticket_list.html', {'tickets': tickets})
