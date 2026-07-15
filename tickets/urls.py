from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('list/', views.ticket_list, name='ticket_list'),
    path('create/', views.create_ticket, name='ticket_create'),
    path('<int:id>/detail/', views.ticket_detail, name='ticket_detail'),
    path('<int:id>/update/', views.ticket_update, name='ticket_update'),
]
