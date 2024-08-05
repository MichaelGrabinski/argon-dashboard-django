from django.contrib import admin
from .models import Tool
from apps.home.models import Tool, Profile, MaintenanceRecord, Property, Unit, Vehicle, VehicleImage, Repair, MaintenanceHistory, ScheduledMaintenance, TagHouse, Location, PropertyLocation, PropertyInfo, Location
from apps.home.models import Task, Attachment, Comment, ActivityLog, Project, Note, Document, ReferenceMaterial, GameProject, Task, Budget, Expense, FinancialReport, Tag, OpenRepair, RentPayment, ProjectDocument


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




