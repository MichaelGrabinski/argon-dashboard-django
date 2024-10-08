# -*- encoding: utf-8 -*-
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect 
from .forms import ToolSearchForm
from apps.home.models import Tool, Material, TaskLink, Profile, MaintenanceRecord, Property, Unit, Vehicle, VehicleImage, Repair, MaintenanceHistory, ScheduledMaintenance, TagHouse, Location, PropertyLocation, PropertyInfo
from django.db.models import Q
from apps.home.models import Task, Attachment, Comment, ActivityLog, Project, Note, Document, ReferenceMaterial, GameProject, Task, Budget, Expense, FinancialReport, ProjectPhase, ReferenceMaterial, ProjectDocument
from .forms import TaskForm, CommentForm, AttachmentForm, AssignTaskForm, QuickTaskForm, ProjectImageForm, MaterialForm, LaborEntryForm, ProjectNoteForm,ProjectAttachmentForm

from apps.home.models import *
from .forms import *
from django.contrib.auth.models import User
from django import forms
from .forms import ReferenceMaterialForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task, Tool, MaintenanceRecord
from .metrics import get_project_progress, get_task_status_distribution, get_budget_vs_actual_spending, get_expense_breakdown
from django.db.models import Count, Sum, F
from .serializers import TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Conversation, Message
from django.contrib.auth.decorators import login_required
from openai import OpenAI
from django.template import Library
#from apps.home.templatetags import markdown_extras
import base64
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import openai
import io
from openai import OpenAIError
from .models import Conversation, Message
import json
from .forms import ImportConversationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from pdfminer.high_level import extract_text
import re
from datetime import datetime

def is_michael(user):
    return user.username == 'Michael'


@login_required(login_url="/login/")
def index(request):
    # Metrics for construction projects
    construction_projects = Project.objects.filter(project_type='construction')
    construction_project_metrics = []
    for project in construction_projects:
        progress = get_project_progress(project)
        remaining_progress = 100 - progress
        task_status_distribution = get_task_status_distribution(project)
        budget_vs_spending = get_budget_vs_actual_spending(project)
        expense_breakdown = get_expense_breakdown(project)
        construction_project_metrics.append({
            'project': project,
            'progress': progress,
            'remaining_progress': remaining_progress,
            'task_status_distribution': task_status_distribution,
            'budget_vs_spending': budget_vs_spending,
            'expense_breakdown': expense_breakdown,
        })

    # Metrics for game studio projects
    game_projects = Project.objects.filter(project_type='game')
    game_project_metrics = []
    for project in game_projects:
        progress = get_project_progress(project)
        remaining_progress = 100 - progress
        task_status_distribution = get_task_status_distribution(project)
        game_project_metrics.append({
            'project': project,
            'progress': progress,
            'remaining_progress': remaining_progress,
            'task_status_distribution': task_status_distribution,
        })

    context = {
        'total_open_tickets': Task.objects.filter(status='open').count(),
        'tickets_assigned_to_you': Task.objects.filter(assigned_to=request.user).count(),
        'total_tools': Tool.objects.count(),
        'total_maintenance_records': MaintenanceRecord.objects.count(),
        'total_users': User.objects.count(),
        'construction_project_metrics': construction_project_metrics,
        'game_project_metrics': game_project_metrics,
    }

    return render(request, 'home/index.html', context)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))












from django.contrib.auth.models import User

@login_required(login_url="/login/")
def profile_view(request):
    try:
        user = User.objects.get(username='mikey')
        profile = get_object_or_404(Profile, user=user)
        print(f"Profile: {profile}")  # Debugging line
        print(f"About Me: {profile.about_me}")  # Debugging line
        print(f"Profile Picture URL: {profile.profile_picture.url if profile.profile_picture else 'No profile picture'}")  # Debugging line
    except User.DoesNotExist:
        print("User 'mikey' does not exist")
        return HttpResponse("User 'mikey' does not exist.", status=404)
    except Profile.DoesNotExist:
        print("Profile does not exist for the user 'mikey'")
        return HttpResponse("Profile does not exist for the user 'mikey'.", status=404)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return HttpResponse("An unexpected error occurred.", status=500)

    context = {
        'profile': profile,
        'user': user
    }
    print(f"Context: {context}")  # Debugging line
    return render(request, 'home/profile.html', context)
    
    


def tool_list(request):
    form = ToolSearchForm(request.GET)
    query = request.GET.get('search', '')
    tag = request.GET.get('tag', None)

    tools = Tool.objects.all()
    if query:
        tools = tools.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if tag:
        tools = tools.filter(tags__id=tag)

    records = MaintenanceRecord.objects.all()
    if query:
        records = records.filter(Q(tool__name__icontains=query) | Q(description__icontains=query))
    if tag:
        records = records.filter(tool__tags__id=tag)

    context = {
        'form': form,
        'tools': tools,
        'records': records,
        'query': query,
        'tag': tag,
    }
    return render(request, 'home/tools.html', context)
    
    
def tool_detail(request, pk):
    tool = get_object_or_404(Tool, pk=pk)
    maintenance_records = tool.maintenance_records.all()
    context = {
        'tool': tool,
        'maintenance_records': maintenance_records,
    }
    return render(request, 'home/tool_detail.html', context)
    
    
def vehicle_overview(request):
    vehicles = Vehicle.objects.all()
    for vehicle in vehicles:
        vehicle.tickets = Task.objects.filter(category=vehicle.model, status='open')  # Using the model as the category identifier
       # vehicle.tickets = Task.objects.filter(category=vehicle.model, status='open')  # Using the model as the category identifier
       #open_tickets = Task.objects.filter(location=unit.location, status='open')  # Update this line

    context = {
        'vehicles': vehicles,
    }
    return render(request, 'home/vehicle_overview.html', context)
    

def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    images = vehicle.images.all()
    current_repairs = vehicle.repairs.filter(status__in=['in_progress', 'pending_parts'])
    maintenance_history = vehicle.maintenance_history.all()
    scheduled_maintenance = vehicle.scheduled_maintenance.all()
    context = {
        'vehicle': vehicle,
        'images': images,
        'current_repairs': current_repairs,
        'maintenance_history': maintenance_history,
        'scheduled_maintenance': scheduled_maintenance,
    }
    return render(request, 'home/vehicle_detail.html', context)
    
def properties_list(request):
    properties = Property.objects.all()
    for property in properties:
        property.open_tickets_count = Task.objects.filter(tags__name=property.name, status='open').count()
    property_locations = PropertyLocation.objects.all()
    context = {
        'properties': properties,
        'property_locations': property_locations,
    }
    return render(request, 'home/properties_list.html', context)

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    units = property.units.all()
    property_info = PropertyInfo.objects.get_or_create(property=property)[0]
    property_location = PropertyLocation.objects.get_or_create(property=property)[0]
    context = {
        'property': property,
        'units': units,
        'property_info': property_info,
        'property_location': property_location,
    }
    return render(request, 'home/property_detail.html', context)

def unit_detail(request, property_pk, unit_pk):
    property = get_object_or_404(Property, pk=property_pk)
    unit = get_object_or_404(Unit, pk=unit_pk, property=property)
    documents = unit.documents.all()
    maintenance_records = MaintenanceRecord.objects.filter(location=unit.unit_number)
    open_repairs = unit.open_repairs.all()
    rent_payments = unit.rent_payments.all()
    open_tickets = Task.objects.filter(location=unit.location, status='open')
    
    # Define 'panoramas' variable
    panoramas = unit.panoramas.prefetch_related('hotspots__target_panorama')

    context = {
        'property': property,
        'unit': unit,
        'documents': documents,
        'maintenance_records': maintenance_records,
        'open_repairs': open_repairs,
        'rent_payments': rent_payments,
        'open_tickets': open_tickets,
        'panoramas': panoramas,
    }
    return render(request, 'home/unit_detail.html', context)
    
@login_required(login_url="/login/")
def task_list(request):
    query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    location_filter = request.GET.get('location', '')
    category_filter = request.GET.get('category', '')  # Get category filter from request

    tasks = Task.objects.all()

    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains(query)))
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if location_filter:
        tasks = tasks.filter(location__name__icontains(location_filter))
    if category_filter:
        tasks = tasks.filter(category__icontains(category_filter))  # Filter by category

    open_tasks = tasks.filter(status='open')
    assigned_tasks = tasks.filter(assigned_to=request.user)
    closed_tasks = tasks.filter(status='closed')
    locations = Location.objects.all()
    categories = Task.objects.values_list('category', flat=True).distinct()  # Get distinct categories

    context = {
        'open_tasks': open_tasks,
        'assigned_tasks': assigned_tasks,
        'closed_tasks': closed_tasks,
        'query': query,
        'status_filter': status_filter,
        'location_filter': location_filter,
        'category_filter': category_filter,  # Pass category filter to context
        'locations': locations,
        'categories': categories,  # Pass categories to context
        'assign_task_form': AssignTaskForm(),
        'tasks': tasks  # Ensure tasks are passed to the template
    }
    return render(request, 'home/task_list.html', context)

    
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = task.comments.all()
    attachments = task.attachments.all()
    activity_logs = task.activity_logs.all()

    if request.method == 'POST':
        if 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.task = task
                comment.user = request.user
                comment.save()
                ActivityLog.objects.create(task=task, user=request.user, action="Added a comment")
                return redirect('task_detail', pk=task.pk)
        elif 'attachment' in request.POST:
            attachment_form = AttachmentForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.task = task
                attachment.save()
                ActivityLog.objects.create(task=task, user=request.user, action="Added an attachment")
                return redirect('task_detail', pk=task.pk)
        elif 'assign_task' in request.POST:
            assign_task_form = AssignTaskForm(request.POST)
            if assign_task_form.is_valid():
                task.assigned_to = assign_task_form.cleaned_data['user']
                task.save()
                ActivityLog.objects.create(task=task, user=request.user, action=f"Assigned the task to {task.assigned_to}")
                return redirect('task_detail', pk=task.pk)
        elif 'update_status' in request.POST:
            task.status = request.POST.get('status')
            task.save()
            ActivityLog.objects.create(task=task, user=request.user, action=f"Updated status to {task.get_status_display()}")
            return redirect('task_detail', pk=task.pk)
    
    comment_form = CommentForm()
    attachment_form = AttachmentForm()
    assign_task_form = AssignTaskForm()
    
    context = {
        'task': task,
        'comments': comments,
        'attachments': attachments,
        'activity_logs': activity_logs,
        'comment_form': comment_form,
        'attachment_form': attachment_form,
        'assign_task_form': assign_task_form,
    }
    return render(request, 'home/task_detail.html', context)

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            ActivityLog.objects.create(task=task, user=request.user, action="Created the task")
            return redirect('task_list')
    else:
        form = TaskForm()
    
    context = {
        'form': form,
    }
    return render(request, 'home/create_task.html', context)


@login_required
def create_quick_task(request):
    if request.method == 'POST':
        form = QuickTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.status = 'open'
            task.save()
            form.save_m2m()  # Save many-to-many relationships (e.g., tags)
            ActivityLog.objects.create(task=task, user=request.user, action="Created the task via quick widget")
            return redirect('task_list')
    else:
        form = QuickTaskForm()
    
    context = {
        'form': form,
    }
    return render(request, 'home/quick_task_widget.html', context)
    
def gantt_chart(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
    }
    return render(request, 'home/gantt_chart.html', context)
    
def construction_hub(request):
    # Set default project_type to 'construction'
    project_type = request.GET.get('project_type', 'construction')
    
    # Filter projects by the specified or default project type
    projects = Project.objects.filter(project_type=project_type)

    if request.method == 'POST':
        if 'document' in request.FILES:
            project_id = request.POST.get('project_id')
            try:
                project = get_object_or_404(Project, pk=project_id)
            except Project.DoesNotExist:
                return render(request, 'home/hub.html', {'error': 'Project not found', 'projects': projects})
            file = request.FILES['document']
            is_model = request.POST.get('is_model', 'off') == 'on'
            ProjectDocument.objects.create(project=project, file=file, is_model=is_model)
            return HttpResponseRedirect(reverse('construction_hub') + f'?project_type={project_type}')
        elif 'file' in request.FILES:
            form = ReferenceMaterialForm(request.POST, request.FILES)
            if form.is_valid():
                reference_material = form.save(commit=False)
                project_id = form.cleaned_data['project'].id
                reference_material.project = get_object_or_404(Project, pk=project_id)
                reference_material.save()
                return HttpResponseRedirect(reverse('construction_hub') + f'?project_type={project_type}')
            else:
                return render(request, 'home/hub.html', {'error': 'Invalid form submission', 'projects': projects})

    reference_form = ReferenceMaterialForm()
    project_data = []
    for project in projects:
        phases = project.phases.all()
        phase_data = []
        total_hours = 0
        completed_hours = 0
        for phase in phases:
            tasks = phase.tasks.filter(parent_task__isnull=True)
            total_phase_tasks = phase.tasks.count()
            completed_phase_tasks = phase.tasks.filter(status='closed').count()
            phase_completion_percentage = (completed_phase_tasks / total_phase_tasks) * 100 if total_phase_tasks > 0 else 0
            phase_data.append({
                'phase': phase,
                'tasks': tasks,
                'completion_percentage': phase_completion_percentage
            })
            for task in phase.tasks.all():
                if task.hours:
                    total_hours += task.hours
                    if task.status == 'closed':
                        completed_hours += task.hours
        remaining_hours = total_hours - completed_hours
        completion_percentage = (completed_hours / total_hours) * 100 if total_hours > 0 else 0
        project_data.append({
            'project': project,
            'phases': phase_data,
            'total_hours': total_hours,
            'completed_hours': completed_hours,
            'remaining_hours': remaining_hours,
            'completion_percentage': completion_percentage
        })

    return render(request, 'home/hub.html', {
        'project_data': project_data,
        'reference_form': reference_form,
        'project_type': project_type  # Pass the project_type to the template
    })
    
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    notes = project.notes.all()
    documents = project.documents.all()
    tasks = project.tasks.all()
    references = project.references.all()

    if request.method == 'POST':
        if 'document' in request.FILES:
            file = request.FILES['document']
            is_model = request.POST.get('is_model', 'off') == 'on'
            ProjectDocument.objects.create(project=project, file=file, is_model=is_model)
            return HttpResponseRedirect(reverse('project_detail', args=[project_id]))

    return render(request, 'home/project_detail.html', {
        'project': project,
        'notes': notes,
        'documents': documents,
        'tasks': tasks,
        'references': references,
    })
    
    
def game_studio_hub(request):
        # Set default project_type to 'construction'
    project_type = request.GET.get('project_type', 'game')
    
    # Filter projects by the specified or default project type
    projects = Project.objects.filter(project_type=project_type)

    if request.method == 'POST':
        if 'document' in request.FILES:
            project_id = request.POST.get('project_id')
            try:
                project = get_object_or_404(Project, pk=project_id)
            except Project.DoesNotExist:
                return render(request, 'game_studio.html', {'error': 'Project not found', 'projects': projects})
            file = request.FILES['document']
            is_model = request.POST.get('is_model', 'off') == 'on'
            ProjectDocument.objects.create(project=project, file=file, is_model=is_model)
            return HttpResponseRedirect(reverse('game_hub') + f'?project_type={project_type}')
        elif 'file' in request.FILES:
            form = ReferenceMaterialForm(request.POST, request.FILES)
            if form.is_valid():
                reference_material = form.save(commit=False)
                project_id = form.cleaned_data['project'].id
                reference_material.project = get_object_or_404(Project, pk=project_id)
                reference_material.save()
                return HttpResponseRedirect(reverse('game_hub') + f'?project_type={project_type}')
            else:
                return render(request, 'home/game_studio.html', {'error': 'Invalid form submission', 'projects': projects})

    reference_form = ReferenceMaterialForm()
    project_data = []
    for project in projects:
        phases = project.phases.all()
        phase_data = []
        total_hours = 0
        completed_hours = 0
        for phase in phases:
            tasks = phase.tasks.filter(parent_task__isnull=True)
            total_phase_tasks = phase.tasks.count()
            completed_phase_tasks = phase.tasks.filter(status='closed').count()
            phase_completion_percentage = (completed_phase_tasks / total_phase_tasks) * 100 if total_phase_tasks > 0 else 0
            phase_data.append({
                'phase': phase,
                'tasks': tasks,
                'completion_percentage': phase_completion_percentage
            })
            for task in phase.tasks.all():
                if task.hours:
                    total_hours += task.hours
                    if task.status == 'closed':
                        completed_hours += task.hours
        remaining_hours = total_hours - completed_hours
        completion_percentage = (completed_hours / total_hours) * 100 if total_hours > 0 else 0
        project_data.append({
            'project': project,
            'phases': phase_data,
            'total_hours': total_hours,
            'completed_hours': completed_hours,
            'remaining_hours': remaining_hours,
            'completion_percentage': completion_percentage
        })

    return render(request, 'home/game_studio.html', {
        'project_data': project_data,
        'reference_form': reference_form,
        'project_type': project_type  # Pass the project_type to the template
    })

def game_project_detail(request, project_id):
    project = get_object_or_404(GameProject, pk=project_id)
    tasks = Task.objects.filter(project=project)
    return render(request, 'home/game_studio_detail.html', {
        'project': project,
        'tasks': tasks,
    })


@login_required
@user_passes_test(is_michael)
def budget_accounting_hub(request):
    projects = Project.objects.all()
    return render(request, 'home/budget_accounting.html', {'projects': projects})

@login_required
@user_passes_test(is_michael)
def budget_project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    budgets = project.budgets.all()
    expenses = project.expenses.all()
    reports = project.financial_reports.all()
    return render(request, 'home/budget_accounting_detail.html', {
        'project': project,
        'budgets': budgets,
        'expenses': expenses,
        'reports': reports,
    })
    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Transaction, Project
from .forms import StatementUploadForm
from .parsers import parse_bank_statement_pdf

def is_michael(user):
    return user.username == 'Michael'

@login_required
@user_passes_test(is_michael)
def upload_statement(request):
    if request.method == 'POST':
        form = StatementUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['statement_file']
            transactions = parse_bank_statement_pdf(file)
            # Assuming transactions relate to a specific project
            project = Project.objects.get(id=form.cleaned_data['project_id'])
            for transaction in transactions:
                Transaction.objects.create(
                    project=project,
                    date=transaction['date'],
                    description=transaction['description'],
                    amount=transaction['amount'],
                    # Add other fields if necessary
                )
            return redirect('budget_project_detail', project_id=project.id)
    else:
        form = StatementUploadForm()
    return render(request, 'home/upload_statement.html', {'form': form})


def parse_bank_statement_pdf(file):
    text = extract_text(file)
    transactions = []

    # Adjust the regex pattern based on your bank statement's format
    pattern = re.compile(r'(\d{2}/\d{2}/\d{4})\s+([\w\s]+)\s+(-?\d+[\.,]\d{2})')
    for match in pattern.finditer(text):
        date_str = match.group(1)
        description = match.group(2).strip()
        amount_str = match.group(3).replace(',', '.')

        date = datetime.strptime(date_str, '%d/%m/%Y').date()
        amount = float(amount_str)

        transactions.append({
            'date': date,
            'description': description,
            'amount': amount,
            'category': 'Imported Bank Statement',
        })

    return transactions
    
    
def get_project_progress(project, is_game_project=False):
    if is_game_project:
        total_tasks = Task.objects.filter(game_project=project).count()
        completed_tasks = Task.objects.filter(game_project=project, status='completed').count()
    else:
        total_tasks = Task.objects.filter(project=project).count()
        completed_tasks = Task.objects.filter(project=project, status='completed').count()
    progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    return progress

def get_task_status_distribution(project, is_game_project=False):
    if is_game_project:
        status_distribution = Task.objects.filter(game_project=project).values('status').annotate(count=Count('status'))
    else:
        status_distribution = Task.objects.filter(project=project).values('status').annotate(count=Count('status'))
    return status_distribution

def get_budget_vs_actual_spending(project):
    budget_data = Budget.objects.filter(project=project).values('category').annotate(budgeted=Sum('amount'))
    expense_data = Expense.objects.filter(project=project).values('category').annotate(spent=Sum('amount'))
    data = {item['category']: {'budgeted': item['budgeted'], 'spent': 0} for item in budget_data}
    for item in expense_data:
        if item['category'] in data:
            data[item['category']]['spent'] = item['spent']
        else:
            data[item['category']] = {'budgeted': 0, 'spent': item['spent']}
    return data

def get_expense_breakdown(project):
    expense_breakdown = Expense.objects.filter(project=project).values('category').annotate(amount=Sum('amount'))
    return expense_breakdown
    

@api_view(['GET'])
def data_list(request, offset):
    if request.method == 'GET':
        tasks = Task.objects.all()
        taskData = TaskSerializer(tasks, many=True)
        return Response({
            "data": taskData.data
        })
    



def public_home(request):
    return render(request, 'home/public_home.html')

def public_about(request):
    return render(request, 'home/about.html')

def public_services(request):
    return render(request, 'home/services.html')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, ProjectDocument
from .forms import ReferenceMaterialForm, ProjectNoteForm, ProjectAttachmentForm, MaterialForm, LaborEntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, ProjectDocument
from .forms import ReferenceMaterialForm, ProjectNoteForm, ProjectAttachmentForm, MaterialForm, LaborEntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectDocument, LaborEntry, Material
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal

@login_required
def other_hub(request):
    # Set default project_type to 'construction'
    project_type = request.GET.get('project_type', 'construction')
    projects = Project.objects.filter(project_type=project_type)

    # Get parameters to determine which project and tab to display
    selected_project_id = request.GET.get('project_id')
    selected_tab = request.GET.get('tab', 'main')  # Default to 'main' tab

    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        if project_id:
            try:
                project = get_object_or_404(Project, id=project_id)
            except ObjectDoesNotExist:
                return render(request, 'home/OtherProjects.html', {'error': 'Project not found', 'projects': projects})

            if 'document' in request.FILES:
                file = request.FILES['document']
                is_model = request.POST.get('is_model', 'off') == 'on'
                ProjectDocument.objects.create(project=project, file=file, is_model=is_model)
                return HttpResponseRedirect(reverse('other_hub') + f'?project_type={project_type}&project_id={project.id}&tab=documents')

            elif 'file' in request.FILES:
                form = ReferenceMaterialForm(request.POST, request.FILES)
                if form.is_valid():
                    reference_material = form.save(commit=False)
                    reference_material.project = project
                    reference_material.save()
                    return HttpResponseRedirect(reverse('other_hub') + f'?project_type={project_type}&project_id={project.id}&tab=reference')
                else:
                    return render(request, 'home/OtherProjects.html', {'error': 'Invalid form submission', 'projects': projects})

            elif 'add_attachment' in request.POST:
                attachment_form = ProjectAttachmentForm(request.POST, request.FILES)
                if attachment_form.is_valid():
                    attachment = attachment_form.save(commit=False)
                    attachment.project = project
                    attachment.uploaded_by = request.user
                    attachment.save()
                    return HttpResponseRedirect(
                        reverse('other_hub') + f'?project_type={project_type}&project_id={project.id}&tab=main'
                    )

            elif 'add_note' in request.POST:
                note_form = ProjectNoteForm(request.POST)
                if note_form.is_valid():
                    note = note_form.save(commit=False)
                    note.project = project
                    note.created_by = request.user
                    note.save()
                    return HttpResponseRedirect(
                        reverse('other_hub') + f'?project_type={project_type}&project_id={project.id}&tab=main'
                    )

            elif 'add_material' in request.POST:
                material_form = MaterialForm(request.POST)
                if material_form.is_valid():
                    material = material_form.save(commit=False)
                    material.project = project
                    material.save()
                    return HttpResponseRedirect(
                        reverse('other_hub') + f'?project_type={project_type}&project_id={project.id}&tab=budget'
                    )

            elif 'add_labor' in request.POST:
                labor_form = LaborEntryForm(request.POST)
                if labor_form.is_valid():
                    labor_entry = labor_form.save(commit=False)
                    labor_entry.project = project
                    labor_entry.save()
                    return HttpResponseRedirect(
                        reverse('other_hub') + f'?project_type={project_type}&project_id={project.id}&tab=budget'
                    )
                else:
                    print(labor_form.errors)  # Debugging: print form errors

            elif 'import_project' in request.POST:
                import_form = ImportProjectForm(request.POST, request.FILES)
                if import_form.is_valid():
                    data = import_form.cleaned_data['file'].read().decode('utf-8')
                    for obj in serializers.deserialize('json', data):
                        obj.save()
                    messages.success(request, 'Project imported successfully.')
                    return redirect('other_hub')
            else:
                print("Unknown POST action.")
        else:
            print("Error: project_id not found in POST data")

    reference_form = ReferenceMaterialForm()
    import_form = ImportProjectForm()
    project_data = []
    for project in projects:
        phases = project.phases.all()
        phase_data = []
        total_hours = 0
        completed_hours = 0
        for phase in phases:
            tasks = phase.tasks.filter(parent_task__isnull=True)
            total_phase_tasks = phase.tasks.count()
            completed_phase_tasks = phase.tasks.filter(status='closed').count()
            phase_completion_percentage = (completed_phase_tasks / total_phase_tasks) * 100 if total_phase_tasks > 0 else 0
            phase_data.append({
                'phase': phase,
                'tasks': tasks,
                'completion_percentage': phase_completion_percentage
            })
            for task in phase.tasks.all():
                if task.hours:
                    total_hours += task.hours
                    if task.status == 'closed':
                        completed_hours += task.hours
        remaining_hours = total_hours - completed_hours
        completion_percentage = (completed_hours / total_hours) * 100 if total_hours > 0 else 0

        notes = project.project_notes.all()
        # Access attachments using the corrected related_name
        attachments = project.project_attachments.all()
        note_form = ProjectNoteForm()
        attachment_form = ProjectAttachmentForm()

        materials = project.materials.select_related('category')
        labor_entries = project.labor_entries.select_related('user')
        material_form = MaterialForm()
        labor_form = LaborEntryForm()
        total_material_cost = sum(Decimal(m.total_cost or 0) for m in materials)
        total_labor_cost = sum(Decimal(l.total_pay or 0) for l in labor_entries)
        total_cost = total_material_cost + total_labor_cost
        cost_per_sqft = (total_cost / Decimal(project.square_footage)) if project.square_footage else Decimal('0')
        total_labor_hours = sum(Decimal(entry.hours_worked or 0) for entry in labor_entries)

        project_data.append({
            'project': project,
            'phases': phase_data,
            'total_hours': total_hours,
            'completed_hours': completed_hours,
            'remaining_hours': remaining_hours,
            'completion_percentage': completion_percentage,
            'notes': notes,
            'attachments': attachments,
            'note_form': note_form,
            'attachment_form': attachment_form,
            'materials': materials,
            'labor_entries': labor_entries,
            'material_form': material_form,
            'labor_form': labor_form,
            'total_material_cost': total_material_cost,
            'total_labor_cost': total_labor_cost,
            'total_cost': total_cost,
            'cost_per_sqft': cost_per_sqft,
            'total_labor_hours': total_labor_hours,
        })

    return render(request, 'home/OtherProjects.html', {
        'project_data': project_data,
        'reference_form': reference_form,
        'import_form': import_form,
        'project_type': project_type,
        'selected_project_id': selected_project_id,
        'selected_tab': selected_tab,
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core import serializers
import json

@login_required
def export_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Serialize the Project instance
    project_data = serializers.serialize(
        'json', [project], use_natural_foreign_keys=True, use_natural_primary_keys=True
    )
    project_json = json.loads(project_data)[0]  # Get the first (and only) element

    # Serialize Manager (if exists)
    if project.manager:
        manager_data = serializers.serialize(
            'json', [project.manager], use_natural_foreign_keys=True, use_natural_primary_keys=True
        )
        project_json['manager'] = json.loads(manager_data)[0]
    else:
        project_json['manager'] = None

    # Serialize Team Members
    team_members = project.team_members.all()
    team_members_data = serializers.serialize(
        'json', team_members, use_natural_foreign_keys=True, use_natural_primary_keys=True
    )
    project_json['team_members'] = json.loads(team_members_data)

    # Serialize Tasks
    tasks = project.tasks.all()  # Use the correct related_name 'tasks'
    tasks_data = serializers.serialize(
        'json', tasks, use_natural_foreign_keys=True, use_natural_primary_keys=True
    )
    project_json['tasks'] = json.loads(tasks_data)

    # Serialize Budgets
    budgets = project.budgets.all()  # Use the correct related_name 'budgets'
    budgets_data = serializers.serialize(
        'json', budgets, use_natural_foreign_keys=True, use_natural_primary_keys=True
    )
    project_json['budgets'] = json.loads(budgets_data)

    # Serialize Project Attachments
    attachments = project.attachments.all()  # Use the correct related_name 'attachments'
    attachments_data = serializers.serialize(
        'json', attachments, use_natural_foreign_keys=True, use_natural_primary_keys=True
    )
    project_json['attachments'] = json.loads(attachments_data)

    # Convert the final project data back to JSON string
    final_data = json.dumps(project_json, indent=4)

    # Return as JSON file download
    response = HttpResponse(final_data, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename=project_{project_id}.json'
    return response
    
import json
import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Project

def import_projects(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            messages.error(request, "No file was uploaded. Please select a JSON file to import.")
            return render(request, 'home/import_projects.html')

        try:
            data = json.load(uploaded_file)

            # Ensure data is a list
            if isinstance(data, dict):
                data = [data]
            elif isinstance(data, list):
                pass
            else:
                messages.error(request, "Invalid JSON structure.")
                return render(request, 'home/import_projects.html')

            for item in data:
                # Access the 'fields' dictionary containing the project data
                fields = item.get('fields', {})
                if not fields:
                    messages.error(request, "Missing 'fields' in the JSON data.")
                    continue  # Skip this item

                # Extract project fields
                title = fields.get('title')
                if not title:
                    messages.error(request, "Title is missing in the project data.")
                    continue  # Skip this item

                description = fields.get('description', '')

                # Manager is a list containing usernames
                manager_usernames = fields.get('manager', [])
                manager = None
                if manager_usernames:
                    manager_username = manager_usernames[0]  # Assuming the first one is the manager
                    try:
                        manager = User.objects.get(username=manager_username)
                    except User.DoesNotExist:
                        messages.warning(request, f"Manager '{manager_username}' does not exist.")
                else:
                    messages.warning(request, f"No manager specified for project '{title}'.")

                # Parse dates
                start_date_str = fields.get('start_date')
                end_date_str = fields.get('end_date')
                date_format = '%Y-%m-%d'

                start_date = None
                end_date = None

                if start_date_str:
                    try:
                        start_date = datetime.datetime.strptime(start_date_str, date_format).date()
                    except ValueError:
                        messages.warning(request, f"Invalid start date '{start_date_str}' for project '{title}'.")

                if end_date_str:
                    try:
                        end_date = datetime.datetime.strptime(end_date_str, date_format).date()
                    except ValueError:
                        messages.warning(request, f"Invalid end date '{end_date_str}' for project '{title}'.")

                project_type = fields.get('project_type', 'other').lower()

                # Parse numeric fields
                square_footage_str = fields.get('square_footage', '0')
                allotted_budget_str = fields.get('allotted_budget', '0.0')

                square_footage = float(square_footage_str) if square_footage_str else 0
                allotted_budget = float(allotted_budget_str) if allotted_budget_str else 0.0

                # Create or update the Project instance
                project, created = Project.objects.update_or_create(
                    title=title,
                    defaults={
                        'description': description,
                        'manager': manager,
                        'start_date': start_date,
                        'end_date': end_date,
                        'project_type': project_type,
                        'square_footage': square_footage,
                        'allotted_budget': allotted_budget,
                        # Add other fields if needed
                    }
                )

                # Handle team members
                team_members_data = fields.get('team_members', [])
                for member_username_list in team_members_data:
                    member_username = member_username_list[0]  # Extract username from list
                    try:
                        team_member = User.objects.get(username=member_username)
                        # Assuming you have a ManyToManyField `team_members` on the Project model
                        project.team_members.add(team_member)
                    except User.DoesNotExist:
                        messages.warning(request, f"Team member '{member_username}' does not exist.")
                # Save the project to persist team member additions
                project.save()

            messages.success(request, "Projects imported successfully from JSON.")
        except json.JSONDecodeError as e:
            messages.error(request, f"Invalid JSON file: {e}")
        except Exception as e:
            messages.error(request, f"An error occurred while processing the file: {e}")
        return render(request, 'home/import_projects.html')
    else:
        return render(request, 'home/import_projects.html')
    
import logging

logger = logging.getLogger(__name__)

def tasks_data(request):
    project_id = request.GET.get('project_id')
    category_filter = request.GET.get('category', '')  # Get category filter from request

    if project_id:
        tasks = Task.objects.filter(phase__project_id=project_id)
    else:
        tasks = Task.objects.all()

    if category_filter:
        tasks = tasks.filter(category__icontains=category_filter)  # Correct filter syntax

    tasks = tasks.values(
        'id', 'title', 'status', 'priority', 'due_date', 'start_date', 'hours', 'assigned_to__username', 'phase__name', 'completed', 'parent_task_id'
    )
    
    tasks_list = list(tasks)

    # Calculate phase start date, due date, and total hours
    phases = ProjectPhase.objects.filter(project_id=project_id) if project_id else ProjectPhase.objects.all()
    phase_data = []
    for phase in phases:
        phase_tasks = Task.objects.filter(phase=phase)
        if phase_tasks.exists():
            start_date = phase_tasks.order_by('start_date').first().start_date
            due_date = phase_tasks.order_by('-due_date').first().due_date
            total_hours = sum(task.hours for task in phase_tasks if task.hours)
            phase_data.append({
                'phase_name': phase.name,
                'start_date': start_date.strftime('%Y-%m-%d') if start_date else None,
                'due_date': due_date.strftime('%Y-%m-%d') if due_date else None,
                'total_hours': total_hours
            })
    
    return JsonResponse({
        'tasks': tasks_list,
        'phases': phase_data
    })

    
@csrf_exempt
def update_task_status(request):
    if request.method == 'POST':
        task_id = request.POST.get('id')
        completed = request.POST.get('completed') == 'true'
        try:
            task = Task.objects.get(id=task_id)
            task.completed = completed
            task.save()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    
    
@csrf_exempt
def update_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('id')
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        duration = request.POST.get('duration')
        progress = request.POST.get('progress')
        parent = request.POST.get('parent')
        phase_id = request.POST.get('phase')

        try:
            task = Task.objects.get(id=task_id)
            task.title = title
            task.start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
            task.hours = duration
            task.progress = progress

            # Validate parent_task_id
            if parent:
                try:
                    parent_task = Task.objects.get(id=parent)
                    task.parent_task = parent_task
                except Task.DoesNotExist:
                    task.parent_task = None
            else:
                task.parent_task = None

            # Validate phase_id
            if phase_id:
                try:
                    phase = ProjectPhase.objects.get(id=phase_id)
                    task.phase = phase
                except ProjectPhase.DoesNotExist:
                    task.phase = None

            task.save()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        duration = request.POST.get('duration')
        progress = request.POST.get('progress')
        parent = request.POST.get('parent')
        project_id = request.POST.get('project_id')
        phase_id = request.POST.get('phase')

        print(f"Received data: title={title}, start_date={start_date}, duration={duration}, progress={progress}, parent={parent}, project_id={project_id}, phase_id={phase_id}")

        try:
            project = Project.objects.get(id=project_id)
            new_task = Task(
                title=title,
                start_date=datetime.strptime(start_date, '%Y-%m-%d %H:%M'),
                hours=duration,
                progress=progress,
                project=project
            )

            # Validate parent_task_id
            if parent:
                try:
                    parent_task = Task.objects.get(id=parent)
                    new_task.parent_task = parent_task
                except Task.DoesNotExist:
                    new_task.parent_task = None

            # Validate phase_id
            if phase_id:
                try:
                    phase = ProjectPhase.objects.get(id=phase_id)
                    new_task.phase = phase
                except ProjectPhase.DoesNotExist:
                    new_task.phase = None

            new_task.save()
            print(f"Task created successfully: {new_task}")
            return JsonResponse({'status': 'success', 'task_id': new_task.id})
        except Project.DoesNotExist:
            print("Project not found")
            return JsonResponse({'status': 'error', 'message': 'Project not found'}, status=404)
        except ValueError as e:
            print(f"ValueError: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def update_link(request):
    if request.method == 'POST':
        link_id = request.POST.get('id')
        source = request.POST.get('source')
        target = request.POST.get('target')
        link_type = request.POST.get('type')
        action = request.POST.get('action')

        if action == 'add':
            TaskLink.objects.create(source_id=source, target_id=target, type=link_type)
        elif action == 'delete':
            try:
                link = TaskLink.objects.get(id=link_id)
                link.delete()
            except TaskLink.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Link not found'}, status=404)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    
    
    
    
    
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.conf import settings
import os
import logging
from gtts import gTTS
import time
from PIL import Image  # For image processing
import openai
from django.core.files.uploadedfile import InMemoryUploadedFile

logger = logging.getLogger(__name__)

# Instantiate the OpenAI client
openai_client = openai.OpenAI(
    api_key=settings.OPENAI_API_KEY
)

# List of allowed models
ALLOWED_MODELS = [
    'gpt-4',
    'gpt-4-vision',
    'chatgpt-4o-latest',
    'o1-preview',
    'dall-e-generation',
    'dall-e-edit',
    'tts-1',
]

@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'home/conversation_list.html', {'conversations': conversations})

@login_required
def new_conversation(request):
    if request.method == 'POST':
        title = request.POST.get('title') or 'New Conversation'
        model_name = request.POST.get('model_name') or 'gpt-4'
        if model_name not in ALLOWED_MODELS:
            model_name = 'gpt-4'  # Default to gpt-4 if invalid model is selected
        conversation = Conversation.objects.create(user=request.user, title=title, model_name=model_name)
        return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        return redirect('conversation_list')

def get_gpt_response(messages, model_name, user_input, image_file=None, include_context=True, max_context_messages=10):
    if model_name in ['gpt-4', 'chatgpt-4o-latest', 'o1-preview']:
        conversation_history = []
        if include_context:
            conversation_history = [
                {"role": msg.sender, "content": msg.content}
                for msg in messages
            ]
            # Limit to the last N messages
            conversation_history = conversation_history[-max_context_messages:]
            conversation_history.append({"role": "user", "content": user_input})

        try:
            response = openai_client.chat.completions.create(
                model=model_name,
                messages=conversation_history,
            )
            assistant_message = response.choices[0].message.content
            return assistant_message.strip()
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            return "An error occurred while processing your request."

    elif model_name == 'gpt-4-vision':
        # GPT-4 Vision is not available via the API yet
        return "GPT-4 Vision is not currently supported via the API."

    elif model_name == 'dall-e-generation':
        # Handle DALL·E Image Generation
        try:
            response = openai_client.images.generate(
                prompt=user_input,
                n=1,
                size="1024x1024",
            )
            image_url = response.data[0].url
            return image_url  # Return the image URL
        except openai.OpenAIError as e:
            logger.error(f"Error generating image: {e}")
            return "An error occurred while generating the image."

    elif model_name == 'dall-e-edit':
        # Handle DALL·E Image Editing
        if image_file:
            try:
                # Save the uploaded image temporarily
                temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
                os.makedirs(temp_dir, exist_ok=True)
                temp_image_path = os.path.join(temp_dir, f"input_{int(time.time())}.png")
                with open(temp_image_path, 'wb') as f:
                    for chunk in image_file.chunks():
                        f.write(chunk)

                # Open the image and ensure it's in RGBA mode with transparency
                image = Image.open(temp_image_path).convert("RGBA")
                # Create a mask image (currently empty - you can create a mask if needed)
                mask = Image.new("RGBA", image.size, (0, 0, 0, 0))

                # Save images to bytes
                image_bytes = io.BytesIO()
                image.save(image_bytes, format='PNG')
                image_bytes.seek(0)

                mask_bytes = io.BytesIO()
                mask.save(mask_bytes, format='PNG')
                mask_bytes.seek(0)

                # Call the OpenAI API to edit the image
                response = openai_client.images.edit(
                    image=image_bytes,
                    mask=mask_bytes,
                    prompt=user_input,
                    n=1,
                    size="1024x1024",
                )
                image_url = response.data[0].url

                # Remove the temporary image file
                os.remove(temp_image_path)

                return image_url  # Return the edited image URL
            except openai.OpenAIError as e:
                logger.error(f"Error editing image: {e}")
                return "An error occurred while editing the image."
            except Exception as e:
                logger.error(f"Unexpected error editing image: {e}")
                return "An unexpected error occurred while editing the image."
        else:
            return "Please upload an image to edit."

    elif model_name == 'tts-1':
        # Handle Text-to-Speech using gTTS
        try:
            tts = gTTS(text=user_input, lang='en')
            audio_filename = f"tts_output_{int(time.time())}.mp3"
            audio_filepath = os.path.join(settings.MEDIA_ROOT, audio_filename)
            tts.save(audio_filepath)
            audio_url = settings.MEDIA_URL + audio_filename
            return audio_url  # Return the URL to the audio file
        except Exception as e:
            logger.error(f"Error generating audio: {e}")
            return "An error occurred while generating the audio."

    else:
        return "Selected model not supported."

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)

    if request.method == 'POST':
        user_input = request.POST.get('message')
        include_context = not request.POST.get('clear_context')

        # Handle multiple file uploads
        uploaded_files = request.FILES.getlist('files')

        # Initialize a variable to hold combined file contents
        files_content = ""

        for uploaded_file in uploaded_files:
            # Security check: Validate file size (e.g., max 2MB)
            if uploaded_file.size > 2 * 1024 * 1024:  # 2 MB limit per file
                continue  # Skip files that are too large

            # Read file content
            try:
                file_content = uploaded_file.read().decode('utf-8', errors='ignore')
                # Append file name and content to files_content
                files_content += f"\n### File: {uploaded_file.name}\n{file_content}\n"
            except Exception as e:
                logger.error(f"Error reading file {uploaded_file.name}: {e}")
                continue  # Skip files that can't be read

        # Construct the full user input including files
        full_user_input = user_input
        if files_content:
            full_user_input += f"\n\nPlease consider the following files:\n{files_content}"

        # Save user's message
        Message.objects.create(
            conversation=conversation,
            sender='user',
            content=full_user_input,
            message_type='text'
        )

        # Fetch updated messages including the new user message
        messages = conversation.messages.order_by('created_at')

        # Get assistant's response using the selected model
        response = get_gpt_response(
            messages, conversation.model_name, full_user_input, include_context=include_context
        )

        # Save assistant's message
        Message.objects.create(
            conversation=conversation,
            sender='assistant',
            content=response,
            message_type='text'
        )

        return redirect('conversation_detail', conversation_id=conversation.id)

    else:
        messages = conversation.messages.order_by('created_at')
        return render(
            request,
            'home/conversation_detail.html',
            {'conversation': conversation, 'messages': messages}
        )
        
@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    if request.method == 'POST':
        conversation.delete()
        return redirect('conversation_list')
    else:
        return render(request, 'home/confirm_delete.html', {'conversation': conversation})
        
@login_required
def clear_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    if request.method == 'POST':
        # Delete all messages in the conversation
        conversation.messages.all().delete()
        return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        return redirect('conversation_detail', conversation_id=conversation.id)
        
        
@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    conversation = message.conversation
    if conversation.user != request.user:
        return redirect('conversation_detail', conversation_id=conversation.id)

    if request.method == 'POST':
        message.delete()
        return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        return redirect('conversation_detail', conversation_id=conversation.id)

@login_required
def export_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    messages = conversation.messages.order_by('created_at')

    # Prepare data for export
    conversation_data = {
        'title': conversation.title,
        'model_name': conversation.model_name,
        'messages': [
            {
                'sender': msg.sender,
                'content': msg.content,
                'message_type': msg.message_type,
                'created_at': msg.created_at.isoformat(),
            }
            for msg in messages
        ],
    }

    # Convert data to JSON and create the response
    response = HttpResponse(json.dumps(conversation_data), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{conversation.title}.json"'
    return response
    
@login_required
def import_conversation(request):
    if request.method == 'POST':
        form = ImportConversationForm(request.POST, request.FILES)
        if form.is_valid():
            conversation_file = request.FILES['conversations_file']
            try:
                # Read the file and parse JSON
                data = json.load(conversation_file)

                # Create a new conversation
                conversation = Conversation.objects.create(
                    user=request.user,
                    title=data.get('title', 'Imported Conversation'),
                    model_name=data.get('model_name', 'gpt-4'),
                )

                # Create messages
                for msg_data in data['messages']:
                    Message.objects.create(
                        conversation=conversation,
                        sender=msg_data['sender'],
                        content=msg_data['content'],
                        message_type=msg_data.get('message_type', 'text'),
                        # Optionally set created_at if you trust the data
                        # created_at=msg_data.get('created_at', timezone.now()),
                    )

                return redirect('conversation_detail', conversation_id=conversation.id)

            except Exception as e:
                logger.error(f"Error importing conversation: {e}")
                # Handle error (e.g., show a message to the user)
                return render(request, 'home/import_conversation.html', {
                    'form': form,
                    'error_message': 'An error occurred while importing the conversation.',
                })
        else:
            # Form is not valid
            return render(request, 'home/import_conversation.html', {'form': form})
    else:
        form = ImportConversationForm()
        return render(request, 'home/import_conversation.html', {'form': form})

def import_projects(request):
    if request.method == 'POST':
        file = request.FILES['file']
        data = json.load(file)
        for item in data:
            project, created = Project.objects.get_or_create(
                title=item['title'],
                defaults={
                    'description': item['description'],
                    'start_date': item['start_date'],
                    'end_date': item['end_date'],
                    # Set other fields as needed
                }
            )
        return redirect('construction_hub')
    return render(request, 'home/import_projects.html')
        
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, ProjectImage
from .forms import ProjectImageForm

def upload_project_image(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectImageForm(request.POST, request.FILES)
        if form.is_valid():
            project_image = form.save(commit=False)
            project_image.project = project
            project_image.save()
            return redirect('construction_hub')
    else:
        form = ProjectImageForm()
    return render(request, 'home/upload_project_image.html', {'form': form, 'project': project})

from .forms import MaterialForm, LaborEntryForm

def budget_page(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    materials = project.materials.select_related('category')
    labor_entries = project.labor_entries.select_related('user')

    if request.method == 'POST':
        if 'add_material' in request.POST:
            material_form = MaterialForm(request.POST)
            labor_form = LaborEntryForm()  # Empty form
            if material_form.is_valid():
                material = material_form.save(commit=False)
                material.project = project
                material.save()
                return redirect('budget_page', project_id=project.id)
        elif 'add_labor' in request.POST:
            material_form = MaterialForm()  # Empty form
            labor_form = LaborEntryForm(request.POST)
            if labor_form.is_valid():
                labor_entry = labor_form.save(commit=False)
                labor_entry.project = project
                labor_entry.save()
                return redirect('budget_page', project_id=project.id)
    else:
        material_form = MaterialForm()
        labor_form = LaborEntryForm()

    total_material_cost = sum(m.total_cost for m in materials)
    total_labor_cost = sum(l.total_pay for l in labor_entries)
    total_cost = total_material_cost + total_labor_cost
    cost_per_sqft = total_cost / project.square_footage if project.square_footage else 0

    context = {
        'project': project,
        'materials': materials,
        'labor_entries': labor_entries,
        'material_form': material_form,
        'labor_form': labor_form,
        'total_material_cost': total_material_cost,
        'total_labor_cost': total_labor_cost,
        'total_cost': total_cost,
        'cost_per_sqft': cost_per_sqft,
    }
    return render(request, 'home/budget_page.html', context)
    
from .forms import ProjectNoteForm, ProjectAttachmentForm

def project_main(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    notes = project.project_notes.all()
    attachments = project.attachments.all()

    if request.method == 'POST':
        if 'add_note' in request.POST:
            note_form = ProjectNoteForm(request.POST)
            attachment_form = ProjectAttachmentForm()  # Empty form
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.project = project
                note.created_by = request.user
                note.save()
                return redirect('project_main', project_id=project.id)
        elif 'add_attachment' in request.POST:
            note_form = ProjectNoteForm()  # Empty form
            attachment_form = ProjectAttachmentForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.project = project
                attachment.uploaded_by = request.user
                attachment.save()
                return redirect('project_main', project_id=project.id)
    else:
        note_form = ProjectNoteForm()
        attachment_form = ProjectAttachmentForm()

    context = {
        'project': project,
        'notes': notes,
        'attachments': attachments,
        'note_form': note_form,
        'attachment_form': attachment_form,
    }
    return render(request, 'home/project_main.html', context)
    
from django.contrib import messages

def import_project(request):
    if request.method == 'POST':
        form = ImportProjectForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data['file'].read().decode('utf-8')
            for obj in serializers.deserialize('json', data):
                obj.save()
            messages.success(request, 'Project imported successfully.')
            return redirect('projects_list')  # Redirect to your projects list
    else:
        form = ImportProjectForm()
    return render(request, 'home/import_project.html', {'form': form})
    
    
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form})

def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_form.html', {'form': form})
    
    
from django.shortcuts import render, get_object_or_404, redirect
from .models import Invoice, LineItem, Service, Material, LaborEntry
from .forms import InvoiceForm, LineItemForm, ServiceForm, MaterialForm, LaborEntryForm
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

@login_required
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'home/invoice_list.html', {'invoices': invoices})

from decimal import Decimal

@login_required
def invoice_create(request):
    LineItemFormSet = inlineformset_factory(Invoice, LineItem, form=LineItemForm, extra=1, can_delete=True)
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = LineItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.creation_date = timezone.now()
            invoice.save()
            formset.instance = invoice

            total_amount = Decimal('0.00')
            line_items = formset.save(commit=False)
            for item_form, line_item in zip(formset.forms, line_items):
                service = line_item.service
                quantity = line_item.quantity

                # Perform calculations using the Service's method
                cost_data = service.calculate_cost(quantity)

                # Update LineItem fields
                line_item.labor_cost = cost_data['labor_cost']
                line_item.materials_cost = cost_data['materials_cost']
                line_item.overhead = cost_data['overhead']
                line_item.profit = cost_data['profit']
                line_item.total_price = cost_data['total_cost']
                line_item.unit_price = line_item.total_price / quantity

                line_item.save()
                total_amount += line_item.total_price

            invoice.total_amount = total_amount
            invoice.save()
            messages.success(request, 'Invoice created successfully.')
            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm()
        formset = LineItemFormSet()
    return render(request, 'home/invoice_form.html', {'form': form, 'formset': formset})
    
@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    line_items = invoice.lineitem_set.all()
    return render(request, 'home/invoice_detail.html', {'invoice': invoice, 'line_items': line_items})

# ... existing views ...

@login_required
def service_list(request):
    services = Service.objects.all()
    return render(request, 'home/service_list.html', {'services': services})

@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully.')
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'home/service_form.html', {'form': form})

@login_required
def service_edit(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully.')
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'home/service_form.html', {'form': form})
    
    
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.contrib.staticfiles import finders

@login_required
def invoice_pdf_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    line_items = invoice.lineitem_set.all()

    # Get the logo image path
    logo_path = finders.find('images/logo.png')  # Adjust the path to your logo
    logo_url = request.build_absolute_uri(settings.STATIC_URL + 'images/logo.png') if logo_path else ''

    # Render HTML content
    html_string = render_to_string('home/invoice_pdf.html', {
        'invoice': invoice,
        'line_items': line_items,
        'logo_url': logo_url,
    })

    # Generate PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf_file = html.write_pdf()

    # Create HTTP response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="invoice_{invoice.id}.pdf"'
    return response

from django.core.mail import EmailMessage
from io import BytesIO

@login_required
def send_invoice_email(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    line_items = invoice.lineitem_set.all()

    # Generate the PDF
    logo_path = finders.find('images/logo.png')  # Adjust as necessary
    logo_url = request.build_absolute_uri(settings.STATIC_URL + 'images/logo.png') if logo_path else ''
    html_string = render_to_string('home/invoice_pdf.html', {
        'invoice': invoice,
        'line_items': line_items,
        'logo_url': logo_url,
    })
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    # Write PDF to BytesIO buffer
    pdf_file = html.write_pdf()
    pdf_buffer = BytesIO(pdf_file)

    # Create the email
    subject = f"Invoice #{invoice.id} from Your Company"
    message = f"Dear {invoice.customer_name},\n\nPlease find attached your invoice.\n\nBest regards,\nYour Company"
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [invoice.customer_email],
    )

    # Attach the PDF
    email.attach(f"invoice_{invoice.id}.pdf", pdf_buffer.getvalue(), 'application/pdf')

    # Send the email
    email.send(fail_silently=False)

    messages.success(request, f'Invoice emailed to {invoice.customer_email}.')

    return redirect('invoice_detail', invoice_id=invoice.id)