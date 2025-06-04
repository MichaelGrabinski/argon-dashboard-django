from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from apps.home import views
from rest_framework.urlpatterns import format_suffix_patterns
from apps.home.views import export_project, import_project

urlpatterns = [
    # The default home page
    path('', views.public_home, name='home'),  # Change this line to use public_home as the default page
    # Original home page
    path('original_home/', views.index, name='original_home'),  # Add this line to keep the original home page accessible
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
    path('projects/export/', views.export_project, name='export_projects'),
    path('projects/import/', views.import_projects, name='import_projects'),
    path('projects/<int:project_id>/upload_image/', views.upload_project_image, name='upload_project_image'),
    path('projects/<int:project_id>/budget/', views.budget_page, name='budget_page'),
    path('projects/<int:project_id>/main/', views.project_main, name='project_main'),
    path('projects/export/<int:project_id>/', export_project, name='export_project'),
    path('projects/import/', import_project, name='import_project'),
    #path('construction/project/<int:project_id>/', views.project_detail, name='project_detail'),
    
    path('game-studio/', views.game_studio_hub, name='game_studio_hub'),
    path('game-studio/project/<int:project_id>/', views.game_project_detail, name='game_project_detail'),
    path('budget-accounting/', views.budget_accounting_hub, name='budget_accounting_hub'),
    path('budget-accounting/project/<int:project_id>/', views.budget_project_detail, name='budget_project_detail'),
    path('upload-statement/', views.upload_statement, name='upload_statement'),
    # Matches any HTML file
 
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('conversations/new/', views.new_conversation, name='new_conversation'),
    path('conversations/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'), 
    path('conversation/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('conversation/<int:conversation_id>/clear/', views.clear_conversation, name='clear_conversation'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('conversation/export/', views.export_conversation, name='export_conversation'),
    path('conversation/<int:conversation_id>/export/', views.export_conversation, name='export_conversation'),
    path('conversation/import/', views.import_conversation, name='import_conversation'),
    
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/create/', views.invoice_create, name='invoice_create'),
    path('invoices/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('services/', views.service_list, name='service_list'),
    path('services/create/', views.service_create, name='service_create'),
    path('services/<int:service_id>/edit/', views.service_edit, name='service_edit'),
   # path('invoices/<int:invoice_id>/pdf/', views.invoice_pdf_view, name='invoice_pdf'),
    #path('send-invoice-email/<int:invoice_id>/', views.send_invoice_email, name='send_invoice_email'),
    
    path('showcase/', views.showcase, name='showcase'),
    path('generate_letter/', views.generate_letter_pdf, name='generate_letter_pdf'),
    path('generate_project_report/<int:project_id>/', views.generate_project_report_pdf, name='generate_project_report_pdf'),
    path('generate_custom_letter/', views.generate_custom_letter_pdf, name='generate_custom_letter_pdf'),
    path('request-quote/', views.request_quote, name='request_quote'),

    path('store/', views.store_product_list, name='store_product_list'),
    path('store/product/<int:product_id>/', views.store_product_detail, name='store_product_detail'),
    path('store/cart/', views.store_cart_detail, name='store_cart_detail'),
    path('store/checkout/', views.store_checkout, name='store_checkout'),
    
    path('trucking/', views.trucking_hub, name='trucking_hub'),
    path('trucking/export-accounting/', views.export_accounting_csv, name='export_accounting_csv'),
    path('trucking/monthly-pl-data/', views.monthly_pl_data, name='monthly_pl_data'),
    path('trucking/ifta-report/', views.ifta_report, name='ifta_report'),
    # apps/home/urls.py

    # GPS endpoints
    path('api/update_location/', views.update_truck_location, name='update_truck_location'),
    path('api/locations/', views.truck_locations_api, name='truck_locations_api'),
    # Public tracking
    path('track/<str:token>/', views.public_load_tracking, name='public_load_tracking'),
    # Excel exports
    path('export/loads/', views.export_loads_excel, name='export_loads_excel'),
    path('export/fuel/', views.export_fuel_entries_excel, name='export_fuel_entries_excel'),
    path('export/maintenance/', views.export_maintenance_excel, name='export_maintenance_excel'),
    path('export/drivers/', views.export_drivers_excel, name='export_drivers_excel'),
    path('export/customers/', views.export_customers_excel, name='export_customers_excel'),
    path('export/tolls/', views.export_tolls_excel, name='export_tolls_excel'),
    path('export/invoices/', views.export_invoices_excel, name='export_invoices_excel'),
    path('export/hos/', views.export_hos_logs_excel, name='export_hos_logs_excel'),
    # Generate weekly invoices
    path('generate_weekly_invoices/', views.generate_weekly_invoices, name='generate_weekly_invoices'),
]

    
    re_path(r'^.*\.*', views.pages, name='pages'),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
