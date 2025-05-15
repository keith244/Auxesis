from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('squad_meeting/', views.squad_meeting, name='squad-meeting'),
]