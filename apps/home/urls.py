from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from apps.home import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    re_path(r'^data/(.*)$', views.data_list),
    
    # Public Pages
    path('public_home/', views.public_home, name='public_home'), 
    path('public_about/', views.public_about, name='public_about'),
    path('public_services/', views.public_services, name='public_services'),
    
    
    # Tool management
    path('tools/', views.tool_list, name='tool_list'),  # Changed to 'tools/' to avoid conflict with home
    path('tool/<int:pk>/', views.tool_detail, name='tool_detail'),
    path('tasks_data/', views.tasks_data, name='tasks_data'),
    
    path('update_task_status/', views.update_task_status, name='update_task_status'),
    path('update_task/', views.update_task, name='update_task'),
    path('update_link/', views.update_link, name='update_link'),
    path('add_task/', views.add_task, name='add_task'),
    
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
    
    path('construction/', views.construction_hub, name='construction_hub'),
    path('construction/project/<int:project_id>/', views.project_detail, name='project_detail'),
    
    path('projects/', views.other_hub, name='other_hub'),
    #path('construction/project/<int:project_id>/', views.project_detail, name='project_detail'),
    
    path('game-studio/', views.game_studio_hub, name='game_studio_hub'),
    path('game-studio/project/<int:project_id>/', views.game_project_detail, name='game_project_detail'),
    path('budget-accounting/', views.budget_accounting_hub, name='budget_accounting_hub'),
    path('budget-accounting/project/<int:project_id>/', views.budget_project_detail, name='budget_project_detail'),
    # Matches any HTML file
    re_path(r'^.*\.*', views.pages, name='pages'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)