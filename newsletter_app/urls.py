# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('schedule_newsletter/', views.schedule_newsletter, name='schedule_newsletter'),
    path('payment/', views.payment, name='payment'),
]
