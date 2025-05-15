from django.urls import path
from . import views

urlpatterns = [
    path('', views.ilogin, name='login'),
    path('registration/', views.iregister, name='register'),
    path('ilogout/', views.ilogout, name='logout')
]