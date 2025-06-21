from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('index/', views.index, name='index'),
    path('harvest-group-report/', views.harvest_group_report, name='harvest-group-report'),
    path('view-all-reports/', views.view_all_meetings, name='view_all_reports'),
    path('leadership-application/', views.leadership_application, name='leadership_application'),
] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)