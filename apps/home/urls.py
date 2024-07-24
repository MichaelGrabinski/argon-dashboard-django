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
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('properties/<int:property_pk>/floors/<int:floor_pk>/', views.floor_detail, name='floor_detail'),
    path('properties/<int:property_pk>/floors/<int:floor_pk>/units/<int:unit_pk>/', views.unit_detail, name='unit_detail'),
   
    # Matches any HTML file
    re_path(r'^.*\.*', views.pages, name='pages'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)