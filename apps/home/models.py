# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db import models
import os
#from .models import Location
from .custom_storage import StaticFileSystemStorage
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import secrets

def get_static_image_path(instance, filename):
    return os.path.join('static', 'tools_images', filename)
    

class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
        
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Tool(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('under_repair', 'Under Repair'),
        ('out_of_order', 'Out of Order'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    purchase_date = models.DateField(null=True, blank=True)
    manufacturer = models.CharField(max_length=200, null=True, blank=True)
    model_number = models.CharField(max_length=200, null=True, blank=True)
    assigned_to = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='tools_images/', storage=StaticFileSystemStorage(), null=True, blank=True)
    location_image = models.ImageField(upload_to='tools_images/', storage=StaticFileSystemStorage(), null=True, blank=True)
    location_x = models.FloatField(null=True, blank=True)
    location_y = models.FloatField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name
        
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

       
class Project(models.Model):
    PROJECT_TYPE_CHOICES = (
        ('construction', 'Construction'),
        ('game', 'Game'),
        ('other', 'Other'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_projects')
    team_members = models.ManyToManyField(User, related_name='projects')
    start_date = models.DateField()
    end_date = models.DateField()
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES, default='construction')
    square_footage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    allotted_budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    # Additional fields for cost calculations
    # For construction projects
    cost_per_square_foot = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # For 'other' projects (per item)
    item_name = models.CharField(max_length=100, null=True, blank=True)
    number_of_items = models.PositiveIntegerField(null=True, blank=True)
    cost_per_item = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # For game projects, we can use 'allotted_budget' as the total cost

    def calculate_total_cost(self):
        if self.project_type == 'construction':
            if self.square_footage and self.cost_per_square_foot:
                return self.square_footage * self.cost_per_square_foot
        elif self.project_type == 'game':
            if self.allotted_budget:
                return self.allotted_budget
        elif self.project_type == 'other':
            if self.number_of_items and self.cost_per_item:
                return self.number_of_items * self.cost_per_item
        return 0  # Default to zero if not enough data

    def __str__(self):
        return self.title
        
class Property(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    owner_contact = models.CharField(max_length=200)
    manager_name = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    image_or_video = models.FileField(upload_to='property_media/', storage=StaticFileSystemStorage(), null=True, blank=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    unit_number = models.CharField(max_length=10)
    tenant_name = models.CharField(max_length=200, null=True, blank=True)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lease_agreement = models.FileField(upload_to='unit_media/', storage=StaticFileSystemStorage(), null=True, blank=True)
    image_or_video = models.FileField(upload_to='unit_media/', storage=StaticFileSystemStorage(), null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    tour_image = models.ImageField(upload_to='tour_images/', storage=StaticFileSystemStorage() , null=True, blank=True)
    
    def __str__(self):
        return f"Unit {self.unit_number} - {self.property}"
        
class Document(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='unit_documents/', storage=StaticFileSystemStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)

class MaintenanceRecord(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='maintenance_logs', null=True, blank=True)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name='maintenance_records', null=True, blank=True)
    date = models.DateField()
    description = models.TextField()
    performed_by = models.CharField(max_length=200)
    location = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.tool or self.unit} - {self.date}"

class OpenRepair(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='open_repairs')
    description = models.TextField()
    reported_date = models.DateField()
    image = models.ImageField(upload_to='repair_images/', storage=StaticFileSystemStorage(), null=True, blank=True)

    def __str__(self):
        return f"Repair for {self.unit} - {self.reported_date}"

class RentPayment(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='rent_payments')
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('paid', 'Paid'), ('due', 'Due')])

    def __str__(self):
        return f"{self.unit} - {self.date} - {self.status}"
  
class PropertyInfo(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='info')
    legal_files = models.FileField(upload_to='legal_files/', storage=StaticFileSystemStorage(), null=True, blank=True)
    extra_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Info for {self.property.name}"
    
class PropertyLocation(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='property_location')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"Location for {self.property.name}"
        
class Vehicle(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('under_maintenance', 'Under Maintenance'),
    )

    make = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    year = models.IntegerField()
    vin = models.CharField(max_length=17, unique=True)
    license_plate = models.CharField(max_length=10, unique=True)
    owner_name = models.CharField(max_length=200)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='vehicle_images/', storage=StaticFileSystemStorage(), null=True, blank=True)
    media = models.FileField(upload_to='vehicle_media/', storage=StaticFileSystemStorage(), null=True, blank=True)  # Renamed field to accept both video and GIFs

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"
        
      
class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vehicle_gallery/', storage=StaticFileSystemStorage())

    def __str__(self):
        return f"Image for {self.vehicle}"

class Repair(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='repairs')
    description = models.TextField()
    assigned_personnel = models.CharField(max_length=200)
    start_date = models.DateField()
    estimated_completion_date = models.DateField()
    status = models.CharField(max_length=50, choices=[('in_progress', 'In Progress'), ('pending_parts', 'Pending Parts'), ('completed', 'Completed')])

    def __str__(self):
        return f"Repair for {self.vehicle} - {self.start_date}"

class MaintenanceHistory(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_history')
    date = models.DateField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_provider = models.CharField(max_length=200)
    document = models.FileField(upload_to='maintenance_documents/', storage=StaticFileSystemStorage(), null=True, blank=True)

    def __str__(self):
        return f"Maintenance for {self.vehicle} - {self.date}"

class ScheduledMaintenance(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='scheduled_maintenance')
    description = models.TextField()
    due_date = models.DateField()
    assigned_personnel = models.CharField(max_length=200)
    frequency = models.CharField(max_length=50, choices=[('one_time', 'One-time'), ('recurring', 'Recurring')])

    def __str__(self):
        return f"Scheduled Maintenance for {self.vehicle} - {self.due_date}"
        
class TagHouse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
        
class ProjectPhase(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='phases')
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_critical = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project.title} - {self.name}" 
        
        
        
class Task(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('in_progress', 'In Progress'),
        ('waiting_for_materials', 'Waiting for Materials'),
        ('on_hold', 'On Hold'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='open')
    due_date = models.DateField(null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)  # Add this line
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    progress = models.FloatField(default=0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    completed_date = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(TagHouse, related_name='tasks', blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    phase = models.ForeignKey(ProjectPhase, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subtasks', null=True, blank=True)
    completed = models.BooleanField(default=False)  # Add this line
    
    def __str__(self):
        return self.title

class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/', storage=StaticFileSystemStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ActivityLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='activity_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

class Note(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()

class ProjectDocument(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/', storage=StaticFileSystemStorage())
    version = models.IntegerField(default=1)
    is_model = models.BooleanField(default=False)

class ReferenceMaterial(models.Model):
    PROJECT_REFERENCE_TYPE_CHOICES = [
        ('video', 'Video'),
        ('schematic', 'Schematic'),
        ('note', 'Note'),
        ('image', 'Image'),
        ('model', '3D Model'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='references')
    type = models.CharField(max_length=50, choices=PROJECT_REFERENCE_TYPE_CHOICES)
    content = models.TextField()  # URL for videos, text for notes, etc.
    
    
class GameProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_game_projects')
    team_members = models.ManyToManyField(User, related_name='game_projects')
    start_date = models.DateField()
    end_date = models.DateField()

# Budget/Accounting Models
class Budget(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='budgets')
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    def __str__(self):
        return f"{self.date} - {self.description} - ${self.amount}"



class FinancialReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='financial_reports')
    report_file = models.FileField(upload_to='financial_reports/')
    created_at = models.DateTimeField(auto_now_add=True)
    
class Transaction(models.Model):
    # Define your fields here
    project = models.ForeignKey('Project', related_name='transactions', on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255, default='Imported Bank Statement')

    def __str__(self):
        return f"{self.date} - {self.description} - {self.amount}"   
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', storage=StaticFileSystemStorage(), null=True, blank=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', storage=StaticFileSystemStorage(), null=True, blank=True)
    about_me = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username
        

class TaskLink(models.Model):
    LINK_TYPES = (
        ('0', 'Finish to Start (default)'),
        ('1', 'Start to Start'),
        ('2', 'Finish to Finish'),
        ('3', 'Start to Finish'),
    )

    source = models.ForeignKey(Task, related_name='link_sources', on_delete=models.CASCADE)
    target = models.ForeignKey(Task, related_name='link_targets', on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=LINK_TYPES, default='0')

    def __str__(self):
        return f"{self.get_type_display()} link from {self.source} to {self.target}"   

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=255)
    model_name = models.CharField(max_length=50, default='gpt-4')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('audio', 'Audio'),
    )
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=50)  # 'user' or 'assistant'
    content = models.TextField()
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:50]}"
        
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/', storage=StaticFileSystemStorage(),)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.project.title}"

class MaterialCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Material(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='materials')
    category = models.ForeignKey(MaterialCategory, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_cost = self.unit_cost * self.quantity
        super().save(*args, **kwargs)

class LaborEntry(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='labor_entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hours_worked = models.DecimalField(max_digits=10, decimal_places=2)
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    total_pay = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_pay = self.hours_worked * self.pay_rate
        super().save(*args, **kwargs)
        
class ProjectNote(models.Model): 
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_notes') 
    content = models.TextField() 
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note for {self.project.title}"

class ProjectAttachment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_attachments')
    file = models.FileField(upload_to='project_attachments/', storage=StaticFileSystemStorage())
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)   
        
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_rate = models.DecimalField(max_digits=10, decimal_places=2)
    labor_cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    material_cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Add fields for overhead and profit percentages if they vary by service
    overhead_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10)  # Default to 10%
    profit_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=15)    # Default to 15%

    def __str__(self):
        return self.name  
        
    def calculate_cost(self, quantity):
        labor_cost = self.labor_cost_per_unit * quantity
        materials_cost = self.material_cost_per_unit * quantity
        base_cost = labor_cost + materials_cost
        if base_cost < self.minimum_charge:
            base_cost = self.minimum_charge
        overhead = base_cost * (self.overhead_percentage / 100)
        profit = base_cost * (self.profit_percentage / 100)
        total_cost = base_cost + overhead + profit
        return {
            'labor_cost': labor_cost,
            'materials_cost': materials_cost,
            'base_cost': base_cost,
            'overhead': overhead,
            'profit': profit,
            'total_cost': total_cost
            
        }
class Invoice(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(blank=True)
    customer_address = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creation_date = models.DateField(auto_now_add=True)
    valid_until = models.DateField(default=timezone.now() + timezone.timedelta(days=60))
    services = models.ManyToManyField(Service, through='LineItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Invoice {self.id} for {self.customer_name}"

class LineItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in square feet")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    materials_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    overhead = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    profit = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def __str__(self):
        return f"{self.service.name} - {self.description}"
        
class Panorama(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='panoramas')
    image = models.ImageField(upload_to='tour_images/', storage=StaticFileSystemStorage())
    name = models.CharField(max_length=100, help_text="Name of the panorama (e.g., 'Living Room')")
    description = models.TextField(blank=True, null=True)
    initial_view_parameters = models.JSONField(blank=True, null=True, help_text="JSON configuration for initial pitch and yaw")
    
    def __str__(self):
        return f"{self.name} - {self.unit}"

class Hotspot(models.Model):
    panorama = models.ForeignKey(Panorama, on_delete=models.CASCADE, related_name='hotspots')
    target_panorama = models.ForeignKey(Panorama, on_delete=models.CASCADE, related_name='incoming_hotspots')
    pitch = models.FloatField(help_text="Vertical angle in degrees")
    yaw = models.FloatField(help_text="Horizontal angle in degrees")
    text = models.CharField(max_length=100, help_text="Text to display on hover")

    def __str__(self):
        return f"Hotspot from {self.panorama.name} to {self.target_panorama.name}"

from django.db import models

class Income(models.Model):
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.description} - ${self.amount}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', storage=StaticFileSystemStorage(), null=True, blank=True)  # Add this field

    def __str__(self):
        return self.name

class OptionGroup(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, related_name='option_groups', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.name}"

class Option(models.Model):
    group = models.ForeignKey(OptionGroup, related_name='options', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    percentage_adjustment = models.DecimalField(max_digits=5, decimal_places=2, default=0.00,
                                                help_text='Enter as a decimal, e.g., 0.12 for 12%')

    def __str__(self):
        return f"{self.group.name}: {self.name}"

    def get_price_adjustment(self, base_cost):
        """
        Calculate the price adjustment based on percentage or fixed amount.
        """
        if self.percentage_adjustment and self.percentage_adjustment != Decimal('0.000'):
            percentage = Decimal(str(self.percentage_adjustment))
            adjustment = base_cost * percentage
            return adjustment.quantize(Decimal('0.01'))  # Round to 2 decimal places
        else:
            price_adj = Decimal(str(self.price_adjustment))
            return price_adj.quantize(Decimal('0.01'))  # Round to 2 decimal places

class CartItem(models.Model):
    # For simplicity, we'll not associate the cart with a user or session for now
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    width = models.DecimalField(max_digits=6, decimal_places=2)  # Door Width (in inches)
    height = models.DecimalField(max_digits=6, decimal_places=2)  # Door Height (in inches)
    options = models.ManyToManyField(Option, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    
    
    def compute_total_price(self):
        """
        Compute the total price based on base price, options, and dimensions.
        """
        # Convert width, height, and quantity to Decimal
        width = Decimal(str(self.width))
        height = Decimal(str(self.height))
        quantity = Decimal(str(self.quantity))

        # Convert base_price to Decimal
        base_price = Decimal(str(self.product.base_price))

        # Calculate the area
        area = width * height  # area is now a Decimal

        # Calculate base cost
        base_cost = base_price * area

        # Initialize total_adjustment as Decimal
        total_adjustment = Decimal('0.00')

        # Adjust price based on selected options
        for option in self.options.all():
            adjustment = option.get_price_adjustment(base_cost)
            total_adjustment += adjustment

        # Compute the total price
        price = (base_cost + total_adjustment) * quantity
        self.total_price = price.quantize(Decimal('0.01'))  # Round to 2 decimal places

        return self.total_price



class PriceListEntry(models.Model):
    PROJECT_TYPE_CHOICES = (
        ('remodel', 'Remodel'),
        ('repair', 'Repair'),
        ('new_build', 'New Build'),
    )
    QUALITY_CHOICES = (
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    )
    SIZE_CHOICES = (
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    )
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='price_list_entries')
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES)
    quality = models.CharField(max_length=20, choices=QUALITY_CHOICES, null=True, blank=True)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, null=True, blank=True)
    labor_cost_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    material_cost_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    overhead_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10.00'))
    profit_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('15.00'))
    
    def calculate_adjusted_costs(self, quantity):
        # Retrieve base costs from the service
        labor = self.service.labor_cost_per_unit * quantity
        material = self.service.material_cost_per_unit * quantity
        
        # Apply adjustments
        labor += self.labor_cost_adjustment
        material += self.material_cost_adjustment
        
        base_cost = labor + material
        overhead = base_cost * (self.overhead_percentage / Decimal('100'))
        profit = base_cost * (self.profit_percentage / Decimal('100'))
        total_cost = base_cost + overhead + profit
        
        return {
            'labor_cost': labor,
            'material_cost': material,
            'base_cost': base_cost,
            'overhead': overhead,
            'profit': profit,
            'total_cost': total_cost
        }

    def __str__(self):
        return f"{self.service.name} - {self.project_type} ({self.quality or 'N/A'}, {self.size or 'N/A'})"


# home/models.py
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import datetime

# ──────────────────────────────────────────────────────────────
# 1) Truck, Driver, and Customer/Broker
# ──────────────────────────────────────────────────────────────

class Truck(models.Model):
    name = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=50, blank=True)
    odometer = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.license_plate})"


class Driver(models.Model):
    """
    A CDL driver who can be assigned to loads.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cdl_number = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    hire_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Customer(models.Model):
    """
    Shipper or Broker who provides loads.
    """
    name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name


# ──────────────────────────────────────────────────────────────
# 2) Truck Expense & FuelEntry
# ──────────────────────────────────────────────────────────────

class TruckExpense(models.Model):
    """
    General expense (fuel, maintenance, insurance, tolls, etc.).
    """
    truck = models.ForeignKey(
        Truck,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    date_incurred = models.DateField(default=datetime.date.today)
    category_choices = [
        ('fuel', 'Fuel'),
        ('maintenance', 'Maintenance'),
        ('insurance', 'Insurance'),
        ('tolls', 'Tolls'),
        ('permits', 'Permits'),
        ('other', 'Other'),
    ]
    category = models.CharField(max_length=20, choices=category_choices, default='other')

    # Can allocate this expense to one or more loads:
    loads = models.ManyToManyField(
        'TruckLoad',
        blank=True,
        related_name='allocated_expenses',
        help_text="Optionally link this expense to load(s)."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.truck.name} – {self.description} (${self.amount})"


class FuelEntry(models.Model):
    """
    A fill‐up record for fuel tracking.
    """
    truck = models.ForeignKey(
        Truck,
        on_delete=models.CASCADE,
        related_name='fuel_entries'
    )
    date = models.DateField(default=datetime.date.today)
    gallons = models.DecimalField(max_digits=6, decimal_places=2)
    price_per_gallon = models.DecimalField(max_digits=5, decimal_places=2)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    odometer_reading = models.PositiveIntegerField(help_text="Odometer reading at fill‐up")

    def save(self, *args, **kwargs):
        self.total_cost = (self.gallons * self.price_per_gallon).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)

    def miles_since_last_fill(self):
        prev = FuelEntry.objects.filter(
            truck=self.truck,
            date__lt=self.date
        ).order_by('-date').first()
        if prev:
            return self.odometer_reading - prev.odometer_reading
        return None

    def mpg(self):
        miles = self.miles_since_last_fill()
        if miles is not None and self.gallons > 0:
            return (Decimal(miles) / self.gallons).quantize(Decimal('0.01'))
        return None

    def __str__(self):
        return f"{self.truck.name} – {self.date} – {self.gallons} gal"


# ──────────────────────────────────────────────────────────────
# 3) Truck Maintenance (renamed to avoid conflict with your existing MaintenanceRecord)
# ──────────────────────────────────────────────────────────────

class TruckMaintenanceSchedule(models.Model):
    """
    Recurring maintenance triggers (e.g. every 10,000 miles or 6 months).
    """
    truck = models.ForeignKey(
        Truck,
        on_delete=models.CASCADE,
        related_name='maintenance_schedules'
    )
    service_type = models.CharField(max_length=100)
    interval_miles = models.PositiveIntegerField(null=True, blank=True,
        help_text="If set, schedule every X miles")
    interval_months = models.PositiveIntegerField(null=True, blank=True,
        help_text="If set, schedule every X months")

    last_service_date = models.DateField(null=True, blank=True)
    last_service_odometer = models.PositiveIntegerField(null=True, blank=True)

    next_service_date = models.DateField(null=True, blank=True)
    next_service_odometer = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.last_service_date and self.interval_months:
            self.next_service_date = (
                self.last_service_date + datetime.timedelta(days=30 * self.interval_months)
            )
        if self.last_service_odometer and self.interval_miles:
            self.next_service_odometer = self.last_service_odometer + self.interval_miles
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.truck.name} – {self.service_type}"


class TruckMaintenanceRecord(models.Model):
    """
    Actual maintenance event (to complement TruckMaintenanceSchedule).
    """
    truck = models.ForeignKey(
        Truck,
        on_delete=models.CASCADE,
        related_name='maintenance_events'
    )
    schedule = models.ForeignKey(
        TruckMaintenanceSchedule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='records'
    )
    date = models.DateField(default=datetime.date.today)
    odometer = models.PositiveIntegerField(help_text="Odometer at service")
    description = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    parts_replaced = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.schedule:
            self.schedule.last_service_date = self.date
            self.schedule.last_service_odometer = self.odometer
            self.schedule.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.truck.name} – {self.date} – {self.description}"


# ──────────────────────────────────────────────────────────────
# 4) Truck Load & Route Mapping
# ──────────────────────────────────────────────────────────────

class TruckLoad(models.Model):
    """
    Each load: pay, miles, hours, driver, customer, route, etc.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    truck = models.ForeignKey(
        Truck,
        on_delete=models.CASCADE,
        related_name='loads'
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='loads'
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='loads'
    )

    date_started = models.DateField(default=datetime.date.today)
    date_completed = models.DateField(null=True, blank=True)
    time_loaded = models.TimeField(null=True, blank=True)
    time_unloaded = models.TimeField(null=True, blank=True)

    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    miles = models.PositiveIntegerField(default=0)
    hours_total = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    hours_load_unload = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))

    # For route mapping:
    pickup_address = models.CharField(max_length=300, blank=True)
    dropoff_address = models.CharField(max_length=300, blank=True)
    route_distance = models.PositiveIntegerField(null=True, blank=True,
        help_text="Miles from routing API, if used")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    created_at = models.DateTimeField(auto_now_add=True)

    def mark_completed(self):
        self.status = 'completed'
        self.date_completed = datetime.date.today()
        self.save()

    def total_load_expenses(self):
        return self.allocated_expenses.aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')

    def net_profit(self):
        return (self.pay_amount - self.total_load_expenses()).quantize(Decimal('0.01'))

    def cost_per_mile(self):
        if self.miles > 0:
            return (self.total_load_expenses() / Decimal(self.miles)).quantize(Decimal('0.01'))
        return None

    def profit_per_mile(self):
        if self.miles > 0:
            return (self.net_profit() / Decimal(self.miles)).quantize(Decimal('0.01'))
        return None

    def __str__(self):
        return f"Load #{self.pk} | {self.truck.name} → {self.customer.name if self.customer else '—'}"


# ──────────────────────────────────────────────────────────────
# 5) TruckFile (with Annotations)
# ──────────────────────────────────────────────────────────────

class TruckFile(models.Model):
    truck = models.ForeignKey(
        Truck,
        on_delete=models.CASCADE,
        related_name='files'
    )
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='trucking/files/%Y/%m/')
    notes = models.TextField(blank=True, help_text="Optional annotation")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.truck.name} – {self.title}"


# ──────────────────────────────────────────────────────────────
# 6) Hours of Service Log (HOS)
# ──────────────────────────────────────────────────────────────

class HosLog(models.Model):
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name='hos_logs'
    )
    date = models.DateField(default=datetime.date.today)
    on_duty_time = models.TimeField()
    off_duty_time = models.TimeField()
    driving_hours = models.DecimalField(max_digits=4, decimal_places=2,
        help_text="Total hours spent driving today")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.driver.user.username} – {self.date} HOS"


# ──────────────────────────────────────────────────────────────
# 7) Truck Invoice & LineItem (renamed from your existing Invoice/LineItem)
# ──────────────────────────────────────────────────────────────

class TruckInvoice(models.Model):
    """
    Invoice or Rate Confirmation for a completed load.
    """
    load = models.OneToOneField(
        TruckLoad,
        on_delete=models.CASCADE,
        related_name='truck_invoice'
    )
    invoice_number = models.CharField(max_length=50, unique=True)
    date_issued = models.DateField(default=datetime.date.today)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} (Load {self.load.pk})"


class TruckLineItem(models.Model):
    """
    Line item on TruckInvoice.
    """
    invoice = models.ForeignKey(
        TruckInvoice,
        on_delete=models.CASCADE,
        related_name='line_items'
    )
    description = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal('1.00'))
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = (self.quantity * self.unit_price).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} × {self.quantity} @ {self.unit_price}"


# ──────────────────────────────────────────────────────────────
# 8) Toll Entry (per load)
# ──────────────────────────────────────────────────────────────

class TollEntry(models.Model):
    load = models.ForeignKey(
        TruckLoad,
        on_delete=models.CASCADE,
        related_name='tolls'
    )
    date = models.DateField(default=datetime.date.today)
    toll_location = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Load {self.load.pk} – {self.toll_location} – ${self.amount}"

# ──────────────────────────────────────────────────────────────────────────────
# New Models for GPS, Documents, Geofencing, Tracking, Stops, and Incidents
# ──────────────────────────────────────────────────────────────────────────────

class TruckLocation(models.Model):
    truck     = models.ForeignKey(Truck, on_delete=models.CASCADE)
    latitude  = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'timestamp'

    def __str__(self):
        return f"{self.truck.name} @ ({self.latitude}, {self.longitude}) on {self.timestamp}"

class TruckDocument(models.Model):
    truck      = models.ForeignKey(Truck, on_delete=models.CASCADE)
    title      = models.CharField(max_length=200)
    file       = models.FileField(upload_to='truck_documents/')
    expires_on = models.DateField()

    def is_expired(self):
        return self.expires_on < timezone.localdate()

    def days_until_expiry(self):
        return (self.expires_on - timezone.localdate()).days

    def __str__(self):
        return f"{self.truck.name} – {self.title}"

class DriverDocument(models.Model):
    driver     = models.ForeignKey(Driver, on_delete=models.CASCADE)
    title      = models.CharField(max_length=200)
    file       = models.FileField(upload_to='driver_documents/')
    expires_on = models.DateField()

    def is_expired(self):
        return self.expires_on < timezone.localdate()

    def days_until_expiry(self):
        return (self.expires_on - timezone.localdate()).days

    def __str__(self):
        return f"{self.driver.user.username} – {self.title}"

class Geofence(models.Model):
    name    = models.CharField(max_length=100)
    polygon = models.TextField(
        help_text="JSON array of [lat, lng] points defining a polygon. e.g. [[41.8, -73.1], [41.9, -73.1], ...]"
    )

    def __str__(self):
        return self.name

class GeofenceAlert(models.Model):
    truck       = models.ForeignKey(Truck, on_delete=models.CASCADE)
    geofence    = models.ForeignKey(Geofence, on_delete=models.CASCADE)
    location    = models.ForeignKey(TruckLocation, on_delete=models.CASCADE)
    timestamp   = models.DateTimeField(auto_now_add=True)
    acknowledged = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.truck.name} entered {self.geofence.name} @ {self.timestamp}"

class LoadTrackingToken(models.Model):
    load      = models.OneToOneField(TruckLoad, on_delete=models.CASCADE)
    token     = models.CharField(max_length=32, unique=True, default=secrets.token_hex)
    created   = models.DateTimeField(auto_now_add=True)

    def get_tracking_url(self):
        from django.urls import reverse
        return reverse('public_load_tracking', args=[self.token])

    def __str__(self):
        return f"Token for Load {self.load.id}"

class LoadStop(models.Model):
    load      = models.ForeignKey(TruckLoad, on_delete=models.CASCADE, related_name='stops')
    order     = models.PositiveIntegerField()
    address   = models.CharField(max_length=250)
    latitude  = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"Stop {self.order} for Load {self.load.id}"

class IncidentReport(models.Model):
    truck       = models.ForeignKey(Truck, on_delete=models.CASCADE, null=True, blank=True)
    load        = models.ForeignKey(TruckLoad, on_delete=models.CASCADE, null=True, blank=True)
    driver      = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    date        = models.DateField()
    description = models.TextField()
    photos      = models.FileField(upload_to='incident_photos/', null=True, blank=True)
    created_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Incident on {self.date} (Truck: {self.truck or 'N/A'})"
'''        
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    '''
    
    