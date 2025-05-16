from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('index/', views.index, name='index'),
    path('squad_report/', views.squad_report, name='squad-report'),
] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)