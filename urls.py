# ./urls.py ( بهه شدت مهم فایل اصلی پروژه)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    

    # این include کردن فایل urls.py اپلیکیشن tickets، مسیرهاشو در دسترس قرار میدهد
    # Include the URL configuration for the tickets application.
    # همه URL های tickets/ از این به بعد در tickets/urls.py تعریف میشن
    # All routes under "tickets/" are defined in tickets/urls.py.

    path('tickets/', include('tickets.urls')), 
    
    # اگر اپلیکیشن accounts برای لاگین/رجیستر دارید:
    # If you have an accounts app for authentication:
    # path('accounts/', include('accounts.urls')),
    #  یا مسیر مربوط به لاگین جنگو
    # Or the URL for Django's login page
    # ... سایر URLهای پروژه (مثل صفحه اصلی)
    # path('', views.home_view, name='home'),
]
# Serve media files (e.g., images) during development.
# برای نمایش فایل‌های مدیا (مثل عکس‌ها) در حالت دیباگ
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # برای نمایش فایل‌های استاتیک هم اگر لازم بود (معمولا لازم نیست در دیباگ)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
