from django.contrib import admin
from .models import Tool
from .models import Tool, MaintenanceRecord, Tag, Property, Unit, OpenRepair, RentPayment, Vehicle, VehicleImage, Repair, MaintenanceHistory, ScheduledMaintenance, Task, Location


# Register your models here.
admin.site.register(Task)
admin.site.register(Tool)
admin.site.register(MaintenanceRecord)
admin.site.register(Tag)
admin.site.register(Property)
admin.site.register(Unit)
admin.site.register(OpenRepair)
admin.site.register(RentPayment)
admin.site.register(Vehicle)
admin.site.register(VehicleImage)
admin.site.register(Repair)
admin.site.register(MaintenanceHistory)
admin.site.register(ScheduledMaintenance)
admin.site.register(Location)