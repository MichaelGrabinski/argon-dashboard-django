import os
import django

# Set the environment variable to point to your Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django
django.setup()

import csv
import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from apps.home.models import (
    Location, Tag, Tool, Project, Property, Unit, Document, MaintenanceRecord, 
    OpenRepair, RentPayment, PropertyInfo, PropertyLocation, Vehicle, VehicleImage, 
    Repair, MaintenanceHistory, ScheduledMaintenance, TagHouse, Task, Attachment, 
    Comment, ActivityLog, Note, ProjectDocument, ReferenceMaterial, GameProject, 
    Budget, Expense, FinancialReport, ProjectPhase
)
'''
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

def load_units():
    fields = ['unit_number', 'tenant_name', 'rent_amount', 'notes']
    related_fields = {
        'property': get_property,
        'location': get_location,
    }
    file_path = 'sample_data/units.csv'
    load_csv(file_path, Unit, fields, related_fields)

def load_csv(file_path, model, fields, related_fields={}):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Replace '\n' with actual newlines in all string fields
            for key in row:
                if isinstance(row[key], str):
                    row[key] = row[key].replace('\\n', '\n')
            
            # Only include specified fields in the data
            data = {field: row[field] if row[field] != '' else None for field in fields if field in row}
            for related_field, related_func in related_fields.items():
                if related_field in row:
                    if callable(related_func):
                        try:
                            data[related_field] = related_func(row[related_field], row)
                        except TypeError:
                            data[related_field] = related_func(row[related_field])
                    else:
                        data[related_field] = related_func[row[related_field]]
                    if data[related_field] is None:
                        print(f"Skipping row due to missing related data: {row}")
                        break
            else:
                # Debugging: Print the data being processed
                print(f"Processing data for {model.__name__}: {data}")

                # Ensure no unexpected fields are included
                data = {key: value for key, value in data.items() if key in fields or key in related_fields}

                # Provide default values for required fields if they are missing
                if 'property' not in data or data['property'] is None:
                    print(f"Skipping row due to missing property: {row}")
                    continue
                
                obj, created = model.objects.update_or_create(**data)
                if created:
                    print(f"Created {model.__name__}: {obj}")
                else:
                    print(f"Updated {model.__name__}: {obj}")

# Call the function to load data from CSV files
load_units()
'''
# Helper function to create user if not exists
def create_user_if_not_exists(username, password):
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password=password)

# Create users
create_user_if_not_exists('johndoe', 'password')
create_user_if_not_exists('janedoe', 'password')
create_user_if_not_exists('emilyj', 'password')

# Create locations
locations = ['Warehouse', 'Toolbox', 'Workshop', 'Garage', 'Office', 'Electrical Toolbox', 'Spare Room', 
             'Bin Number Two Yellow Cap', 'Bin Number 1/I Grey Bin Left of Rack', 'Bin Number 1 Yellow Cap', 'Bin Number 4 Yellow Cap']
for location in locations:
    Location.objects.get_or_create(name=location)

# Create projects
manager_johndoe = User.objects.get(username='johndoe')
manager_janedoe = User.objects.get(username='janedoe')
manager_emilyj = User.objects.get(username='emilyj')

Project.objects.get_or_create(title='Building a Spider Robot', defaults={
    'description': 'Development and construction of an advanced spider robot',
    'manager': manager_johndoe,
    'start_date': '2023-01-01',
    'end_date': '2023-12-31',
    'project_type': 'construction'
})

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
    except Project.MultipleObjectsReturned:
        print(f"Multiple projects found with the title {title}. Please ensure unique project titles.")
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

def get_phase(name, project_title):
    try:
        project = get_project(project_title)
        if project:
            return ProjectPhase.objects.get(name=name, project=project)
    except ProjectPhase.DoesNotExist:
        print(f"Phase {name} for project {project_title} does not exist.")
        return None

def load_csv(file_path, model, fields, related_fields={}):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Replace '\n' with actual newlines in all string fields
            for key in row:
                if isinstance(row[key], str):
                    row[key] = row[key].replace('\\n', '\n')
            
            # Only include specified fields in the data
            data = {field: row[field] if row[field] != '' else None for field in fields if field in row}
            for related_field, related_func in related_fields.items():
                if related_field in row:
                    if callable(related_func):
                        try:
                            data[related_field] = related_func(row[related_field], row)
                        except TypeError:
                            data[related_field] = related_func(row[related_field])
                    else:
                        data[related_field] = related_func[row[related_field]]
                    if data[related_field] is None:
                        print(f"Skipping row due to missing related data: {row}")
                        break
            else:
                # Debugging: Print the data being processed
                print(f"Processing data for {model.__name__}: {data}")

                # Ensure no unexpected fields are included
                data = {key: value for key, value in data.items() if key in fields or key in related_fields}

                # Provide default values for required fields if they are missing
                if 'owner_name' in data and data['owner_name'] is None:
                    data['owner_name'] = 'Unknown Owner'
                
                # Convert is_critical field to boolean if it exists
                if 'is_critical' in data:
                    data['is_critical'] = data['is_critical'].lower() in ('true', '1', 't')
                
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
        'phase': lambda phase_name, row: get_phase(phase_name, row['project']) if 'phase' in row else None,
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

def load_project_phases():
    fields = ['project', 'name', 'description', 'start_date', 'end_date', 'is_critical']
    related_fields = {
        'project': lambda title: get_project(title),
    }
    file_path = 'sample_data/project_phases.csv'
    load_csv(file_path, ProjectPhase, fields, related_fields)

# Call the functions to load data from CSV files
load_projects()
load_project_phases()
load_tasks()
load_tools()
load_properties()
load_units()
load_vehicles()
load_documents()
load_maintenance_records()
load_open_repairs()
load_rent_payments()
#load_property_infos()
#load_property_locations()
#load_vehicle_images()
#load_repairs()
#load_maintenance_histories()
#load_scheduled_maintenance()
#load_tag_houses()
load_attachments()
load_comments()
#load_activity_logs()
load_notes()
load_project_documents()
load_reference_materials()
load_game_projects()
#load_budgets()
#load_expenses()
#load_financial_reports()
