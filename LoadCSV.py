





import csv
import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from apps.home.models import (
    Location, Tag, Tool, Project, Property, Unit, Document, MaintenanceRecord, 
    OpenRepair, RentPayment, PropertyInfo, PropertyLocation, Vehicle, VehicleImage, 
    Repair, MaintenanceHistory, ScheduledMaintenance, TagHouse, Task, Attachment, 
    Comment, ActivityLog, Note, ProjectDocument, ReferenceMaterial, GameProject, 
    Budget, Expense, FinancialReport
)

from django.contrib.auth.models import User
from apps.home.models import Location, Project

# Create users
User.objects.create_user(username='johndoe', password='password')
User.objects.create_user(username='janedoe', password='password')
User.objects.create_user(username='emilyj', password='password')

# Create locations
Location.objects.create(name='Warehouse')
Location.objects.create(name='Toolbox')
Location.objects.create(name='Workshop')
Location.objects.create(name='Garage')
Location.objects.create(name='Office')

# Create projects
manager_johndoe = User.objects.get(username='johndoe')
manager_janedoe = User.objects.get(username='janedoe')
manager_emilyj = User.objects.get(username='emilyj')

Project.objects.create(title='Building A', description='Construction of Building A', manager=manager_johndoe, start_date='2023-03-01', end_date='2024-03-01', project_type='construction')
Project.objects.create(title='Game Development', description='Development of a new game', manager=manager_janedoe, start_date='2022-01-15', end_date='2023-01-15', project_type='game')
Project.objects.create(title='Office Renovation', description='Renovation of office space', manager=manager_emilyj, start_date='2023-04-01', end_date='2023-10-01', project_type='construction')

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

def parse_decimal(decimal_str):
    return Decimal(decimal_str) if decimal_str else None

def get_user(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"User {username} does not exist.")
        return None

def get_location(name):
    try:
        return Location.objects.get(name=name)
    except Location.DoesNotExist:
        print(f"Location {name} does not exist.")
        return None

def get_property(name):
    try:
        return Property.objects.get(name=name)
    except Property.DoesNotExist:
        print(f"Property {name} does not exist.")
        return None

def get_project(title):
    try:
        return Project.objects.get(title=title)
    except Project.DoesNotExist:
        print(f"Project {title} does not exist.")
        return None

def get_unit(unit_number):
    try:
        return Unit.objects.get(unit_number=unit_number)
    except Unit.DoesNotExist:
        print(f"Unit {unit_number} does not exist.")
        return None

def get_tool(name):
    try:
        return Tool.objects.get(name=name)
    except Tool.DoesNotExist:
        print(f"Tool {name} does not exist.")
        return None

def get_vehicle(vin):
    try:
        return Vehicle.objects.get(vin=vin)
    except Vehicle.DoesNotExist:
        print(f"Vehicle {vin} does not exist.")
        return None

def get_task(title):
    try:
        return Task.objects.get(title=title)
    except Task.DoesNotExist:
        print(f"Task {title} does not exist.")
        return None

def load_csv(file_path, model, fields, related_fields={}):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {field: row[field] for field in fields if field in row}
            for related_field, related_func in related_fields.items():
                data[related_field] = related_func(row[related_field])
                if data[related_field] is None:
                    print(f"Skipping row due to missing related data: {row}")
                    break
            else:
                obj, created = model.objects.update_or_create(**data)
                if created:
                    print(f"Created {model.__name__}: {obj}")
                else:
                    print(f"Updated {model.__name__}: {obj}")

def load_tasks():
    fields = ['title', 'description', 'status', 'due_date', 'priority', 'category', 'hours', 'created_at', 'updated_at']
    related_fields = {
        'assigned_to': get_user,
        'created_by': get_user,
        'location': get_location,
        'project': get_project,
    }
    file_path = 'sample_data/tasks.csv'
    load_csv(file_path, Task, fields, related_fields)

def load_tools():
    fields = ['name', 'description', 'status', 'purchase_date', 'manufacturer', 'model_number', 
              'assigned_to', 'location', 'location_x', 'location_y']
    related_fields = {
        'location': get_location,
    }
    file_path = 'sample_data/tools.csv'
    load_csv(file_path, Tool, fields, related_fields)

def load_projects():
    fields = ['title', 'description', 'start_date', 'end_date', 'project_type']
    related_fields = {
        'manager': get_user,
    }
    file_path = 'sample_data/projects.csv'
    load_csv(file_path, Project, fields, related_fields)

def load_properties():
    fields = ['name', 'location', 'owner_name', 'owner_contact', 'manager_name', 'notes']
    file_path = 'sample_data/properties.csv'
    load_csv(file_path, Property, fields)

def load_units():
    fields = ['unit_number', 'tenant_name', 'rent_amount', 'notes']
    related_fields = {
        'property': get_property,
        'location': get_location,
    }
    file_path = 'sample_data/units.csv'
    load_csv(file_path, Unit, fields, related_fields)

def load_vehicles():
    fields = ['make', 'model', 'year', 'vin', 'license_plate', 'owner_name', 'purchase_date', 
              'purchase_price', 'status']
    file_path = 'sample_data/vehicles.csv'
    load_csv(file_path, Vehicle, fields)

def load_documents():
    fields = ['file', 'uploaded_at']
    related_fields = {
        'unit': get_unit,
    }
    file_path = 'sample_data/documents.csv'
    load_csv(file_path, Document, fields, related_fields)

def load_maintenance_records():
    fields = ['date', 'description', 'performed_by', 'location']
    related_fields = {
        'tool': get_tool,
        'unit': get_unit,
    }
    file_path = 'sample_data/maintenance_records.csv'
    load_csv(file_path, MaintenanceRecord, fields, related_fields)

def load_open_repairs():
    fields = ['description', 'reported_date']
    related_fields = {
        'unit': get_unit,
    }
    file_path = 'sample_data/open_repairs.csv'
    load_csv(file_path, OpenRepair, fields, related_fields)

def load_rent_payments():
    fields = ['date', 'amount', 'status']
    related_fields = {
        'unit': get_unit,
    }
    file_path = 'sample_data/rent_payments.csv'
    load_csv(file_path, RentPayment, fields, related_fields)

def load_property_infos():
    fields = ['legal_files', 'extra_notes']
    related_fields = {
        'property': get_property,
    }
    file_path = 'sample_data/property_infos.csv'
    load_csv(file_path, PropertyInfo, fields, related_fields)

def load_property_locations():
    fields = ['latitude', 'longitude']
    related_fields = {
        'property': get_property,
    }
    file_path = 'sample_data/property_locations.csv'
    load_csv(file_path, PropertyLocation, fields, related_fields)

def load_vehicle_images():
    fields = ['image']
    related_fields = {
        'vehicle': get_vehicle,
    }
    file_path = 'sample_data/vehicle_images.csv'
    load_csv(file_path, VehicleImage, fields, related_fields)

def load_repairs():
    fields = ['description', 'assigned_personnel', 'start_date', 'estimated_completion_date', 'status']
    related_fields = {
        'vehicle': get_vehicle,
    }
    file_path = 'sample_data/repairs.csv'
    load_csv(file_path, Repair, fields, related_fields)

def load_maintenance_histories():
    fields = ['date', 'description', 'cost', 'service_provider', 'document']
    related_fields = {
        'vehicle': get_vehicle,
    }
    file_path = 'sample_data/maintenance_histories.csv'
    load_csv(file_path, MaintenanceHistory, fields, related_fields)

def load_scheduled_maintenance():
    fields = ['description', 'due_date', 'assigned_personnel', 'frequency']
    related_fields = {
        'vehicle': get_vehicle,
    }
    file_path = 'sample_data/scheduled_maintenance.csv'
    load_csv(file_path, ScheduledMaintenance, fields, related_fields)

def load_tag_houses():
    fields = ['name']
    file_path = 'sample_data/tag_houses.csv'
    load_csv(file_path, TagHouse, fields)

def load_attachments():
    fields = ['file', 'uploaded_at']
    related_fields = {
        'task': get_task,
    }
    file_path = 'sample_data/attachments.csv'
    load_csv(file_path, Attachment, fields, related_fields)

def load_comments():
    fields = ['content', 'created_at']
    related_fields = {
        'task': get_task,
        'user': get_user,
    }
    file_path = 'sample_data/comments.csv'
    load_csv(file_path, Comment, fields, related_fields)

def load_activity_logs():
    fields = ['action', 'timestamp']
    related_fields = {
        'task': get_task,
        'user': get_user,
    }
    file_path = 'sample_data/activity_logs.csv'
    load_csv(file_path, ActivityLog, fields, related_fields)

def load_notes():
    fields = ['content']
    related_fields = {
        'project': get_project,
    }
    file_path = 'sample_data/notes.csv'
    load_csv(file_path, Note, fields, related_fields)

def load_project_documents():
    fields = ['file', 'version']
    related_fields = {
        'project': get_project,
    }
    file_path = 'sample_data/project_documents.csv'
    load_csv(file_path, ProjectDocument, fields, related_fields)

def load_reference_materials():
    fields = ['type', 'content']
    related_fields = {
        'project': get_project,
    }
    file_path = 'sample_data/reference_materials.csv'
    load_csv(file_path, ReferenceMaterial, fields, related_fields)

def load_game_projects():
    fields = ['title', 'description', 'start_date', 'end_date']
    related_fields = {
        'manager': get_user,
    }
    file_path = 'sample_data/game_projects.csv'
    load_csv(file_path, GameProject, fields, related_fields)

def load_budgets():
    fields = ['category', 'amount']
    related_fields = {
        'project': get_project,
    }
    file_path = 'sample_data/budgets.csv'
    load_csv(file_path, Budget, fields, related_fields)

def load_expenses():
    fields = ['category', 'description', 'amount', 'date']
    related_fields = {
        'project': get_project,
    }
    file_path = 'sample_data/expenses.csv'
    load_csv(file_path, Expense, fields, related_fields)

def load_financial_reports():
    fields = ['report_file', 'created_at']
    related_fields = {
        'project': get_project,
    }
    file_path = 'sample_data/financial_reports.csv'
    load_csv(file_path, FinancialReport, fields, related_fields)

# Call the functions to load data from CSV files
load_tasks()
load_tools()
load_projects()
load_properties()
load_units()
load_vehicles()
load_documents()
load_maintenance_records()
load_open_repairs()
load_rent_payments()
load_property_infos()
load_property_locations()
load_vehicle_images()
load_repairs()
load_maintenance_histories()
load_scheduled_maintenance()
load_tag_houses()
load_attachments()
load_comments()
load_activity_logs()
load_notes()
load_project_documents()
load_reference_materials()
load_game_projects()
load_budgets()
load_expenses()
load_financial_reports()