from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customer_upload/', views.customer_upload, name='customer-upload'),
    path('customer_waitlist/', views.customer_waitlist, name='customer-waitlist'),
    path('log/', views.log, name='log'),
    path('renewals', views.renewals, name='renewals'),
    path('send_email', views.send_email, name='send-email'),
]