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
    category = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='project_attachments/', storage=StaticFileSystemStorage())
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)   
        
        
        
'''        
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    '''