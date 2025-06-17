from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('index/', views.index, name='index'),
    path('harvest_group_report/', views.harvest_group_report, name='harvest-group-report'),
] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)