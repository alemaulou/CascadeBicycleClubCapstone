from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customer_upload/', views.customer_upload, name='customer-upload')
]