
# Initialize Django
django.setup()

# Set the environment variable to point to your Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import os
import django
from apps.home.models import Service, Invoice, LineItem  # Add Service, Invoice, and LineItem imports

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
# Helper function to create user if not exists
def create_user_if_not_exists(username, password, is_superuser=False):
    if not User.objects.filter(username=username).exists():
        if is_superuser:
            User.objects.create_superuser(username=username, password=password)
        else:
            User.objects.create_user(username=username, password=password)

# Create users
create_user_if_not_exists('johndoe', 'password')
create_user_if_not_exists('janedoe', 'password')
create_user_if_not_exists('emilyj', 'password')
create_user_if_not_exists('Nick', 'Dominos07!')
create_user_if_not_exists('Nicholas', 'Gordneer0121')

# Create superuser
create_user_if_not_exists('Michael', 'D3lt@', is_superuser=True)

# Create locations
locations = [
    'Warehouse', 'Toolbox', 'Workshop', 'Garage', 'Office', 'Electrical Toolbox', 
    'Spare Room', 'Bin Number Two Yellow Cap', 'Bin Number 1/I Grey Bin Left of Rack', 
    'Bin Number 1 Yellow Cap', 'Bin Number 4 Yellow Cap', 'Office - Pulaski',
    'Construction Site', 'Unit 3 - Fl. 3 - 98 Pulaski St', '98 Pulaski St',
    'Office - Forest', 'Garage - Forest', 'Garage - Pulaski', 'Workshop - Pulaski'
]
for location in locations:
    Location.objects.get_or_create(name=location)
    
# Create units
units = [
    {'unit_number': 'Unit 1 - Floor 1', 'property_name': '98 Pulaski St'},
    {'unit_number': 'Unit 2 - Floor 2', 'property_name': '98 Pulaski St'},
    {'unit_number': 'Unit 3 - Floor 3', 'property_name': '98 Pulaski St'},
]
for unit in units:
    property_obj, created = Property.objects.get_or_create(name=unit['property_name'])
    Unit.objects.get_or_create(unit_number=unit['unit_number'], property=property_obj)

# Create projects
manager_johndoe = User.objects.get(username='johndoe')
manager_janedoe = User.objects.get(username='janedoe')
manager_emilyj = User.objects.get(username='emilyj')

#Project.objects.get_or_create(title='Building a Spider Robot', defaults={
#    'description': 'Development and construction of an advanced spider robot',
#    'manager': manager_johndoe,
#    'start_date': '2023-01-01',
#    'end_date': '2023-12-31',
#    'project_type': 'construction'
#})

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
        properties = Property.objects.filter(name=name)
        if properties.exists():
            return properties.first()  # Return the first matching property
        else:
            raise Property.DoesNotExist(f"No Property found with name: {name}")
    except Property.MultipleObjectsReturned:
        print(f"Multiple properties found with the name {name}. Returning the first one.")
        return properties.first()
        
def get_service(name):
    try:
        return Service.objects.get(name=name)
    except Service.DoesNotExist:
        print(f"Service {name} does not exist.")
        return None

def get_invoice(invoice_id):
    try:
        invoice_id = int(invoice_id)
        return Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        print(f"Invoice with id {invoice_id} does not exist.")
        return None
    except ValueError:
        print(f"Invalid invoice id: {invoice_id}")
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

def get_task(title, row=None):
    try:
        tasks = Task.objects.filter(title=title)
        if tasks.exists():
            return tasks.first()  # Return the first matching task
        else:
            print(f"No Task found with title: {title}")
            return None
    except Task.MultipleObjectsReturned:
        print(f"Multiple tasks found with the title {title}. Returning the first one.")
        return tasks.first()

def get_phase(name, project_title):
    try:
        project = get_project(project_title)
        if project:
            return ProjectPhase.objects.get(name=name, project=project)
        else:
            print(f"Project {project_title} does not exist.")
            return None
    except ProjectPhase.DoesNotExist:
        print(f"Phase {name} for project {project_title} does not exist.")
        return None
    except ProjectPhase.MultipleObjectsReturned:
        print(f"Multiple phases found with the name {name} for project {project_title}. Returning the first one.")
        return ProjectPhase.objects.filter(name=name, project=project).first()

def load_csv(file_path, model, fields, related_fields={}, field_parsers={}, lookup_fields=None):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Replace '\n' with actual newlines in all string fields
            for key in row:
                if isinstance(row[key], str):
                    row[key] = row[key].replace('\\n', '\n')

            # Only include specified fields in the data
            data = {field: row[field] if row[field] != '' else None for field in fields if field in row}

            # Process fields that need parsing
            for field, parser in field_parsers.items():
                if field in data and data[field] is not None:
                    data[field] = parser(data[field])

            # Process related fields
            for field_name, field_info in related_fields.items():
                if isinstance(field_info, tuple):
                    csv_column_name, related_func = field_info
                else:
                    csv_column_name, related_func = field_name, field_info

                if csv_column_name in row:
                    if callable(related_func):
                        try:
                            data[field_name] = related_func(row[csv_column_name], row)
                        except TypeError:
                            data[field_name] = related_func(row[csv_column_name])
                    else:
                        data[field_name] = related_func[row[csv_column_name]]
                    if data[field_name] is None:
                        print(f"Skipping row due to missing related data: {row}")
                        break
            else:
                # Debugging: Print the data being processed
                print(f"Processing data for {model.__name__}: {data}")

                # Ensure no unexpected fields are included
                all_fields = fields + list(related_fields.keys())
                data = {key: value for key, value in data.items() if key in all_fields}

                # Provide default values for required fields if they are missing
                if 'owner_name' in data and data['owner_name'] is None:
                    data['owner_name'] = 'Unknown Owner'

                # Use lookup fields if provided
                if lookup_fields:
                    lookup_data = {key: data[key] for key in lookup_fields}
                    defaults = {key: value for key, value in data.items() if key not in lookup_fields}
                    obj, created = model.objects.update_or_create(defaults=defaults, **lookup_data)
                else:
                    obj, created = model.objects.update_or_create(**data)
                if created:
                    print(f"Created {model.__name__}: {obj}")
                else:
                    print(f"Updated {model.__name__}: {obj}")

def load_services():
    fields = ['name', 'description', 'base_rate', 'labor_cost_per_unit', 'material_cost_per_unit',
              'minimum_charge', 'overhead_percentage', 'profit_percentage']
    field_parsers = {
        'base_rate': parse_decimal,
        'labor_cost_per_unit': parse_decimal,
        'material_cost_per_unit': parse_decimal,
        'minimum_charge': parse_decimal,
        'overhead_percentage': parse_decimal,
        'profit_percentage': parse_decimal,
    }
    lookup_fields = ['name']
    file_path = 'sample_data/services.csv'
    load_csv(file_path, Service, fields, field_parsers=field_parsers, lookup_fields=lookup_fields)

def load_invoices():
    fields = ['id', 'customer_name', 'customer_email', 'customer_address', 'creation_date', 'valid_until',
              'total_amount', 'notes']
    related_fields = {
        'created_by': ('created_by_username', get_user),
    }
    field_parsers = {
        'id': int,  # Parse 'id' to int
        'creation_date': parse_date,
        'valid_until': parse_date,
        'total_amount': parse_decimal,
    }
    lookup_fields = ['id']
    file_path = 'sample_data/invoices.csv'
    load_csv(file_path, Invoice, fields, related_fields, field_parsers, lookup_fields)

def load_lineitems():
    fields = ['description', 'quantity', 'unit_price', 'labor_cost', 'materials_cost', 'overhead',
              'profit', 'total_price']
    related_fields = {
        'invoice': ('invoice_id', get_invoice),
        'service': ('service_name', get_service),
    }
    field_parsers = {
        'quantity': parse_decimal,
        'unit_price': parse_decimal,
        'labor_cost': parse_decimal,
        'materials_cost': parse_decimal,
        'overhead': parse_decimal,
        'profit': parse_decimal,
        'total_price': parse_decimal,
    }
    lookup_fields = ['invoice', 'description']
    file_path = 'sample_data/lineitems.csv'
    load_csv(file_path, LineItem, fields, related_fields, field_parsers, lookup_fields)

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
        'task': lambda task_title, row: get_task(task_title, row) if 'task' in row else None,
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
load_services()
load_invoices()
load_lineitems()
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
#load_notes()
#load_project_documents()
#load_reference_materials()
#load_game_projects()
#load_budgets()
#load_expenses()
#load_financial_reports()
