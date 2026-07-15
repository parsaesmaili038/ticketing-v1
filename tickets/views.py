# tickets/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm

# -----------------------------------------------------------------------------
# Ticket List View
# -----------------------------------------------------------------------------
@login_required
def ticket_list(request):
    """
    نمایش لیستی از تمام تیکت‌ها، مرتب شده بر اساس تاریخ ایجاد (جدیدترین اول).
    این ویو نیاز به احراز هویت کاربر دارد.
    """
    # دریافت تمام تیکت‌ها از دیتابیس و مرتب‌سازی آن‌ها بر اساس تاریخ ایجاد (نزولی)
    tickets = Ticket.objects.all().order_by('-created_at')

    # رندر کردن قالب ticket_list.html و ارسال لیست تیکت‌ها به آن
    return render(request, 'tickets/ticket_list.html', { # توجه: مسیر قالب را کامل‌تر کردم، اگر اشتباه بود، اصلاح کن
        'tickets': tickets
    })

# -----------------------------------------------------------------------------
# Create Ticket View
# -----------------------------------------------------------------------------
@login_required
def create_ticket(request):
    """
    نمایش فرم ایجاد تیکت جدید یا پردازش داده‌های فرم ارسال شده.
    این ویو نیاز به احراز هویت کاربر دارد.
    فقط کاربرانی که لاگین کرده‌اند می‌توانند تیکت ثبت کنند.
    """
    if request.method == 'POST':
        # اگر درخواست POST بود (یعنی فرم ارسال شده)
        form = TicketForm(request.POST) # ایجاد فرم با داده‌های ارسال شده
        if form.is_valid():
            # اگر فرم معتبر بود، تیکت را ذخیره کن ولی commit نکن تا مالک را اضافه کنیم
            ticket = form.save(commit=False)
            # مالک تیکت را کاربر فعلی (که لاگین کرده) قرار بده
            ticket.owner = request.user
            ticket.save() # ذخیره نهایی تیکت
            # هدایت کاربر به صفحه لیست تیکت‌ها
            return redirect('tickets:ticket_list') # استفاده از namespace درست برای URL
    else:
        # اگر درخواست GET بود (یعنی فقط صفحه را می‌خواهیم ببینیم)
        form = TicketForm() # ایجاد یک فرم خالی

    # رندر کردن قالب create_ticket.html با فرم و عنوان مناسب
    return render(request, 'tickets/create_ticket.html', { # توجه: مسیر قالب را کامل‌تر کردم
        'form': form,
        'title': 'ایجاد تیکت جدید' # عنوان صفحه برای فرم
    })

# -----------------------------------------------------------------------------
# Ticket Detail View
# -----------------------------------------------------------------------------
# @login_required # این decorator را برای نمایش جزئیات تیکت هم اضافه کردم، چون معمولا جزئیات نیاز به لاگین دارند
def ticket_detail(request, id): # <<< تغییر نام پارامتر از ticket_id به id
    """
    نمایش جزئیات یک تیکت خاص بر اساس ID آن.
    از get_object_or_404 برای بازیابی تیکت یا نمایش خطای 404 استفاده می‌شود.
    """
    # بازیابی تیکت با استفاده از ID که از URL گرفته شده
    # از id استفاده می‌کنیم چون در urls.py هم id تعریف شده
    try:
        ticket = Ticket.objects.get(id=id)
    except Ticket.DoesNotExist:
        # اگر تیکتی با این ID پیدا نشد، خطای 404 نمایش داده شود
        from django.http import Http404
        raise Http404("Ticket not found")

    # رندر کردن قالب ticket_detail.html و ارسال جزئیات تیکت
    return render(request, 'tickets/ticket_detail.html', { # توجه: مسیر قالب را کامل‌تر کردم
        'ticket': ticket
    })

# -----------------------------------------------------------------------------
# Ticket Update View
# -----------------------------------------------------------------------------
# @login_required # این decorator را هم برای ویرایش تیکت اضافه کردم
def ticket_update(request, id): # <<< تغییر نام پارامتر از ticket_id به id
    """
    نمایش فرم ویرایش تیکت موجود یا پردازش داده‌های فرم ارسال شده برای به‌روزرسانی.
    این ویو نیاز به احراز هویت کاربر دارد.
    """
    # بازیابی تیکت مورد نظر برای ویرایش
    ticket = get_object_or_404(Ticket, id=id) # استفاده از id طبق تعریف urls.py

    if request.method == 'POST':
        # اگر درخواست POST بود، فرم را با داده‌های جدید و نمونه تیکت پر کن
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            # اگر فرم معتبر بود، تغییرات را ذخیره کن
            form.save()
            # هدایت کاربر به صفحه لیست تیکت‌ها
            return redirect('tickets:ticket_list') # استفاده از namespace درست
    else:
        # اگر درخواست GET بود، فرم را با داده‌های تیکت فعلی پر کن
        form = TicketForm(instance=ticket)

    # رندر کردن قالب create_ticket.html (چون فرم ویرایش هم شبیه فرم ایجاد است)
    # یا می‌توانید یک قالب جداگانه برای ویرایش بسازید.
    return render(request, 'tickets/create_ticket.html', { # توجه: مسیر قالب را کامل‌تر کردم
        'form': form,
        'title': 'ویرایش تیکت' # عنوان صفحه برای فرم ویرایش
    })
