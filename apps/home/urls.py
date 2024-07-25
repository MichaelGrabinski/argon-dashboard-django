from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # The home page
    path('', views.index, name='home'),

    # Tool management
    path('tools/', views.tool_list, name='tool_list'),  # Changed to 'tools/' to avoid conflict with home
    path('tool/<int:pk>/', views.tool_detail, name='tool_detail'),

    path('properties/', views.properties_list, name='properties_list'),
    path('properties/<int:property_pk>/', views.property_detail, name='property_detail'),
    path('properties/<int:property_pk>/units/<int:unit_pk>/', views.unit_detail, name='unit_detail'),  # Update this line
    
    path('vehicles/', views.vehicle_overview, name='vehicle_overview'),
    path('vehicles/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/gantt/', views.gantt_chart, name='gantt_chart'),
    path('tasks/quick_create/', views.create_quick_task, name='create_quick_task'),
    
    # Matches any HTML file
    re_path(r'^.*\.*', views.pages, name='pages'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)