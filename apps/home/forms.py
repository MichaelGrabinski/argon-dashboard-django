from django import forms
from django.contrib.auth.models import User 
from .models import *


class ToolSearchForm(forms.Form):
    search = forms.CharField(required=False, label='Search')
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), required=False, label='Tag')

class TaskForm(forms.ModelForm):
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), required=True, label="Unit")

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date', 'priority', 'unit']

    def save(self, commit=True):
        task = super().save(commit=False)
        task.location = self.cleaned_data['unit'].location  # Set the location based on the selected unit
        if commit:
            task.save()
        return task

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']

class AssignTaskForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label='Assign to')

class QuickTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'priority', 'category', 'hours',
            'assigned_to', 'location', 'due_date', 'project', 'phase',
            'parent_task', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'value': 'New Task'}),
            'description': forms.Textarea(attrs={'value': 'Description of the task'}),
            'priority': forms.Select(),
            'category': forms.TextInput(attrs={'value': 'General'}),
            'hours': forms.NumberInput(attrs={'value': 1}),
            'assigned_to': forms.Select(),
            'location': forms.Select(),  # Use a dropdown for location
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'tags': forms.CheckboxSelectMultiple(),
        }

class ReferenceMaterialForm(forms.ModelForm):
    class Meta:
        model = ReferenceMaterial
        fields = ['project', 'type', 'content']

class ImportConversationForm(forms.Form):
    conversations_file = forms.FileField(
        label='Select a JSON file to import',
        help_text='Max. 5 megabytes'
    )

class StatementUploadForm(forms.Form):
    project_id = forms.ModelChoiceField(queryset=Project.objects.all())
    statement_file = forms.FileField(label='Select PDF Bank Statement')

class BankStatementUploadForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    bank_statement_file = forms.FileField(label='Bank Statement (PDF)')

    def clean_bank_statement_file(self):
        file = self.cleaned_data['bank_statement_file']
        if not file.name.endswith('.pdf'):
            raise forms.ValidationError('Please upload a PDF file.')
        return file

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['category', 'description', 'unit_cost', 'quantity']

from django import forms
from .models import LaborEntry

class LaborEntryForm(forms.ModelForm):
    class Meta:
        model = LaborEntry
        fields = ['user', 'date', 'hours_worked', 'pay_rate']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'hours_worked': forms.NumberInput(attrs={'class': 'form-control'}),
            'pay_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProjectNoteForm(forms.ModelForm):
    class Meta:
        model = ProjectNote
        fields = ['content']

class ProjectAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProjectAttachment
        fields = ['file']
    
class ImportProjectForm(forms.Form):
    file = forms.FileField()
    
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'manager', 'team_members',
            'start_date', 'end_date', 'project_type',
            'square_footage', 'cost_per_square_foot',
            'allotted_budget',
            'item_name', 'number_of_items', 'cost_per_item',
        ]
        widgets = {
            'team_members': forms.CheckboxSelectMultiple(),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'project_type': forms.Select(attrs={'id': 'id_project_type'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        project_type = cleaned_data.get('project_type')

        if project_type == 'construction':
            square_footage = cleaned_data.get('square_footage')
            cost_per_square_foot = cleaned_data.get('cost_per_square_foot')
            if not square_footage or not cost_per_square_foot:
                raise forms.ValidationError('Please provide square footage and cost per square foot for construction projects.')
        elif project_type == 'game':
            allotted_budget = cleaned_data.get('allotted_budget')
            if not allotted_budget:
                raise forms.ValidationError('Please provide the total cost (allotted budget) for game projects.')
        elif project_type == 'other':
            item_name = cleaned_data.get('item_name')
            number_of_items = cleaned_data.get('number_of_items')
            cost_per_item = cleaned_data.get('cost_per_item')
            if not all([item_name, number_of_items, cost_per_item]):
                raise forms.ValidationError('Please provide item details and costs for other projects.')

from django import forms
from .models import Invoice, LineItem, Service, Material, LaborEntry
from django.forms import inlineformset_factory
from .models import Invoice, LineItem

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer_name', 'customer_email', 'customer_address', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class LineItemForm(forms.ModelForm):
    class Meta:
        model = LineItem
        fields = ['service', 'description', 'quantity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return quantity
        
    class Meta:
        model = LineItem
        fields = ['service', 'description', 'quantity']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'name',
            'description',
            'base_rate',
            'labor_cost_per_unit',
            'material_cost_per_unit',
            'minimum_charge',
            'overhead_percentage',
            'profit_percentage',
        ]
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['project', 'category', 'description', 'unit_cost', 'quantity']

class LaborEntryForm(forms.ModelForm):
    class Meta:
        model = LaborEntry
        fields = ['project', 'user', 'hours_worked', 'pay_rate', 'date']
        
        
from django import forms
from .models import Unit, Panorama
from django.forms import inlineformset_factory

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'

PanoramaFormSet = inlineformset_factory(Unit, Panorama, fields=('image', 'name', 'description', 'initial_view_parameters'), extra=1, can_delete=True)

class LetterForm(forms.Form):
    recipient_name = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)

from django import forms
from .models import Income, Expense, Category

class IncomeForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Income
        fields = ['date', 'category', 'description', 'amount']

class ExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Expense
        fields = ['date', 'category', 'description', 'amount']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        
from django import forms
from decimal import Decimal

class AddToCartForm(forms.Form):
    width = forms.DecimalField(max_digits=6, decimal_places=2, min_value=0.01)
    height = forms.DecimalField(max_digits=6, decimal_places=2, min_value=0.01)
    quantity = forms.IntegerField(min_value=1)
    

from django import forms
from .models import (
    Truck, Driver, Customer,
    TruckExpense, FuelEntry, TruckMaintenanceSchedule,
    TruckMaintenanceRecord, TruckLoad, TruckFile,
    HosLog, TruckInvoice, TruckLineItem, TollEntry
)

# ──────────────────────────────────────────────────────────────
# 1) Truck, Driver, Customer Forms
# ──────────────────────────────────────────────────────────────

class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = ['name', 'license_plate', 'odometer', 'active']


class DriverForm(forms.ModelForm):
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Driver
        fields = ['user', 'cdl_number', 'phone', 'hire_date']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'contact_name', 'contact_email', 'contact_phone', 'address']


# ──────────────────────────────────────────────────────────────
# 2) Expense, Fuel, Toll Forms
# ──────────────────────────────────────────────────────────────

class TruckExpenseForm(forms.ModelForm):
    date_incurred = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = TruckExpense
        fields = ['truck', 'description', 'amount', 'date_incurred', 'category', 'loads']


class FuelEntryForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = FuelEntry
        fields = ['truck', 'date', 'gallons', 'price_per_gallon', 'odometer_reading']


class TollEntryForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = TollEntry
        fields = ['load', 'date', 'toll_location', 'amount']


# ──────────────────────────────────────────────────────────────
# 3) Maintenance Schedule & Record Forms
# ──────────────────────────────────────────────────────────────

class TruckMaintenanceScheduleForm(forms.ModelForm):
    last_service_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = TruckMaintenanceSchedule
        fields = [
            'truck', 'service_type',
            'interval_miles', 'interval_months',
            'last_service_date', 'last_service_odometer'
        ]


class TruckMaintenanceRecordForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = TruckMaintenanceRecord
        fields = [
            'truck', 'schedule', 'date',
            'odometer', 'description', 'cost', 'parts_replaced'
        ]


# ──────────────────────────────────────────────────────────────
# 4) Truck Load & File Forms
# ──────────────────────────────────────────────────────────────

class TruckLoadForm(forms.ModelForm):
    date_started = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_completed = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    time_loaded = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    time_unloaded = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)

    class Meta:
        model = TruckLoad
        fields = [
            'truck', 'driver', 'customer',
            'pickup_address', 'dropoff_address',
            'date_started', 'date_completed',
            'time_loaded', 'time_unloaded',
            'miles', 'route_distance',
            'pay_amount', 'hours_total', 'hours_load_unload',
            'status'
        ]


class TruckFileForm(forms.ModelForm):
    class Meta:
        model = TruckFile
        fields = ['truck', 'title', 'file', 'notes']


# ──────────────────────────────────────────────────────────────
# 5) HOS Log Form
# ──────────────────────────────────────────────────────────────

class HosLogForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = HosLog
        fields = ['driver', 'date', 'on_duty_time', 'off_duty_time', 'driving_hours', 'notes']


# ──────────────────────────────────────────────────────────────
# 6) Truck Invoice & LineItem Forms
# ──────────────────────────────────────────────────────────────

class TruckInvoiceForm(forms.ModelForm):
    date_issued = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = TruckInvoice
        fields = ['load', 'invoice_number', 'date_issued', 'total_amount', 'paid', 'paid_date']


class TruckLineItemForm(forms.ModelForm):
    class Meta:
        model = TruckLineItem
        fields = ['description', 'quantity', 'unit_price']

# apps/home/forms.py

from django import forms
from .models import (
    Truck, Driver, Customer,
    TruckDocument, DriverDocument,
    IncidentReport, LoadStop
)

class TruckForm(forms.ModelForm):
    class Meta:
        model  = Truck
        fields = ['name', 'license_plate', 'odometer', 'active']

class DriverForm(forms.ModelForm):
    class Meta:
        model  = Driver
        fields = ['user', 'cdl_number', 'phone', 'hire_date']

class CustomerForm(forms.ModelForm):
    class Meta:
        model  = Customer
        fields = ['name', 'contact_name', 'contact_email', 'contact_phone', 'address']

class TruckDocumentForm(forms.ModelForm):
    class Meta:
        model  = TruckDocument
        fields = ['truck', 'title', 'file', 'expires_on']

class DriverDocumentForm(forms.ModelForm):
    class Meta:
        model  = DriverDocument
        fields = ['driver', 'title', 'file', 'expires_on']

class IncidentForm(forms.ModelForm):
    class Meta:
        model  = IncidentReport
        fields = ['truck', 'load', 'driver', 'date', 'description', 'photos']

class StopForm(forms.ModelForm):
    class Meta:
        model  = LoadStop
        fields = ['load', 'order', 'address', 'latitude', 'longitude']
