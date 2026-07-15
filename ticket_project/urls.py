# ticket_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# این تابع home_redirect خودش مشکلی نداره چون از redirect استفاده می‌کنه
# و redirect از django.shortcuts ایمپورت شده، نه از views پروژه!
def home_redirect(request):
    # فرض می‌کنیم که 'tickets:ticket_list' یک نام URL معتبر در اپلیکیشن tickets هست
    return redirect('tickets:ticket_list') 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'), # مسیر صفحه اصلی که به لیست تیکت‌ها ریدایرکت میشه
    path('tickets/', include('tickets.urls')), # مسیرهای مربوط به اپلیکیشن tickets
]
