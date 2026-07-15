# yourproject/urls.py (فایل اصلی پروژه)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # این include کردن فایل urls.py اپلیکیشن tickets، مسیرهاشو در دسترس قرار میده
    # همه URL های tickets/ از این به بعد در tickets/urls.py تعریف میشن
    path('tickets/', include('tickets.urls')), 
    
    # اگر اپلیکیشن accounts برای لاگین/رجیستر دارید:
    # path('accounts/', include('accounts.urls')), # یا مسیر مربوط به لاگین جنگو
    
    # ... سایر URLهای پروژه (مثل صفحه اصلی)
    # path('', views.home_view, name='home'),
]

# برای نمایش فایل‌های مدیا (مثل عکس‌ها) در حالت دیباگ
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # برای نمایش فایل‌های استاتیک هم اگر لازم بود (معمولا لازم نیست در دیباگ)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
