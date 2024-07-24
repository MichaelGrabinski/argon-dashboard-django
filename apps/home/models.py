# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db import models
import os

# Create your models here.
def get_static_image_path(instance, filename):
    return os.path.join('tools_images', filename)

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
    image = models.ImageField(upload_to=get_static_image_path, null=True, blank=True)

    def __str__(self):
        return self.name

class MaintenanceRecord(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='maintenance_records')
    date = models.DateField()
    description = models.TextField()
    performed_by = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.tool.name} - {self.date}"


class Property(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    number_of_floors = models.IntegerField()
    owner_name = models.CharField(max_length=200)
    owner_contact = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Floor(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='floors')
    floor_number = models.IntegerField()

    def __str__(self):
        return f"{self.property.name} - Floor {self.floor_number}"

class Unit(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='units')
    unit_number = models.CharField(max_length=10)
    tenant_name = models.CharField(max_length=200, null=True, blank=True)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lease_agreement = models.FileField(upload_to='lease_agreements/', null=True, blank=True)
    image = models.ImageField(upload_to='unit_images/', null=True, blank=True)

    def __str__(self):
        return f"Unit {self.unit_number} - {self.floor}"

class UnitImage(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='unit_gallery/')

    def __str__(self):
        return f"Image for {self.unit}"

class MaintenanceLog(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='maintenance_logs')
    date = models.DateField()
    description = models.TextField()
    performed_by = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.unit} - {self.date}"

class OpenRepair(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='open_repairs')
    description = models.TextField()
    reported_date = models.DateField()
    image = models.ImageField(upload_to='repair_images/', null=True, blank=True)

    def __str__(self):
        return f"Repair for {self.unit} - {self.reported_date}"

class RentPayment(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='rent_payments')
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('paid', 'Paid'), ('due', 'Due')])

    def __str__(self):
        return f"{self.unit} - {self.date} - {self.status}"
        
        
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
    image = models.ImageField(upload_to='vehicle_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vehicle_gallery/')

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
    document = models.FileField(upload_to='maintenance_documents/', null=True, blank=True)

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