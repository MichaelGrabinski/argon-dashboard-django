from django.contrib import admin
from .models import Tool
from apps.home.models import *

from django.contrib import admin
from .models import Unit, Panorama

class PanoramaInline(admin.TabularInline):
    model = Panorama
    extra = 1  # Number of extra forms to display

class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'property', 'tenant_name')
    inlines = [PanoramaInline]
    fields = (
        'unit_number', 'property', 'tenant_name', 'rent_amount',
        'lease_agreement', 'image_or_video', 'notes', 'location'
    )

admin.site.register(Unit, UnitAdmin)

from django.contrib import admin
from .models import Unit, Panorama, Hotspot

class HotspotInline(admin.TabularInline):
    model = Hotspot
    fk_name = 'panorama'
    extra = 1

class PanoramaAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    inlines = [HotspotInline]

admin.site.register(Panorama, PanoramaAdmin)
  
# Register your models here.
admin.site.register(Task)
admin.site.register(Tool)
admin.site.register(MaintenanceRecord)
admin.site.register(Tag)
admin.site.register(Property)
admin.site.register(OpenRepair)
admin.site.register(RentPayment)
admin.site.register(Vehicle)
admin.site.register(VehicleImage)
admin.site.register(Repair)
admin.site.register(MaintenanceHistory)
admin.site.register(ScheduledMaintenance)
admin.site.register(Location)
admin.site.register(Profile)

admin.site.register(TagHouse)
admin.site.register(PropertyLocation)
admin.site.register(PropertyInfo)
admin.site.register(Attachment)
admin.site.register(Comment)
admin.site.register(ActivityLog)
admin.site.register(Project)
admin.site.register(Note)
admin.site.register(Document)
admin.site.register(ProjectDocument)
admin.site.register(ReferenceMaterial)
admin.site.register(GameProject)
admin.site.register(Budget)
admin.site.register(Expense)
admin.site.register(FinancialReport)




admin.site.register(ProjectImage)
admin.site.register(MaterialCategory)
admin.site.register(Material)
admin.site.register(LaborEntry)
admin.site.register(ProjectNote)
admin.site.register(ProjectAttachment)
        
admin.site.register(Invoice)
admin.site.register(LineItem)
admin.site.register(Service)


from django.contrib import admin
from .models import Product, OptionGroup, Option

class OptionInline(admin.TabularInline):
    model = Option

class OptionGroupAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

class OptionGroupInline(admin.TabularInline):
    model = OptionGroup

class ProductAdmin(admin.ModelAdmin):
    inlines = [OptionGroupInline]

admin.site.register(Product, ProductAdmin)

from django.contrib import admin
from .models import (
    Truck, Driver, Customer,
    TruckExpense, FuelEntry, TruckMaintenanceSchedule,
    TruckMaintenanceRecord, TruckLoad, TruckFile,
    HosLog, TruckInvoice, TruckLineItem, TollEntry
)

@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_plate', 'odometer', 'active')
    list_filter = ('active',)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'cdl_number', 'phone', 'hire_date')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 'contact_email', 'contact_phone')


@admin.register(TruckExpense)
class TruckExpenseAdmin(admin.ModelAdmin):
    list_display = ('truck', 'date_incurred', 'description', 'amount', 'category')
    list_filter = ('truck', 'category', 'date_incurred')


@admin.register(FuelEntry)
class FuelEntryAdmin(admin.ModelAdmin):
    list_display = ('truck', 'date', 'gallons', 'price_per_gallon', 'total_cost', 'odometer_reading')
    list_filter = ('truck', 'date')


@admin.register(TruckMaintenanceSchedule)
class TruckMaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ('truck', 'service_type', 'interval_miles', 'interval_months', 'next_service_date')
    list_filter = ('truck', 'service_type')


@admin.register(TruckMaintenanceRecord)
class TruckMaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('truck', 'date', 'odometer', 'description', 'cost')
    list_filter = ('truck', 'date')


@admin.register(TruckLoad)
class TruckLoadAdmin(admin.ModelAdmin):
    list_display = ('truck', 'driver', 'customer', 'date_started', 'status', 'pay_amount')
    list_filter = ('status', 'truck', 'driver')


@admin.register(TruckFile)
class TruckFileAdmin(admin.ModelAdmin):
    list_display = ('truck', 'title', 'uploaded_at')
    list_filter = ('truck', 'uploaded_at')


@admin.register(HosLog)
class HosLogAdmin(admin.ModelAdmin):
    list_display = ('driver', 'date', 'driving_hours')


@admin.register(TruckInvoice)
class TruckInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'load', 'date_issued', 'total_amount', 'paid')
    list_filter = ('paid',)


@admin.register(TruckLineItem)
class TruckLineItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'description', 'quantity', 'unit_price', 'total_price')


@admin.register(TollEntry)
class TollEntryAdmin(admin.ModelAdmin):
    list_display = ('load', 'date', 'toll_location', 'amount')
    list_filter = ('load', 'date')
