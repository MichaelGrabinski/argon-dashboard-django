# -*- encoding: utf-8 -*-
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect 
from .forms import ToolSearchForm
from apps.home.models import Tool, MaintenanceRecord, Property, Unit, Vehicle, VehicleImage, Repair, MaintenanceHistory, ScheduledMaintenance, TagHouse, Location, PropertyLocation, PropertyInfo
from django.db.models import Q
from apps.home.models import Task, Attachment, Comment, ActivityLog, Project, Note, Document, ReferenceMaterial, GameProject, Task, Budget, Expense, FinancialReport, ProjectPhase, ReferenceMaterial, ProjectDocument
from .forms import TaskForm, CommentForm, AttachmentForm, AssignTaskForm, QuickTaskForm
from django.contrib.auth.models import User
from django import forms
from .forms import ReferenceMaterialForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task, Tool, MaintenanceRecord
from .metrics import get_project_progress, get_task_status_distribution, get_budget_vs_actual_spending, get_expense_breakdown
from django.db.models import Count, Sum, F

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
    open_tickets = Task.objects.filter(location=unit.location, status='open')  # Update this line

    context = {
        'property': property,
        'unit': unit,
        'documents': documents,
        'maintenance_records': maintenance_records,
        'open_repairs': open_repairs,
        'rent_payments': rent_payments,
        'open_tickets': open_tickets,
    }
    return render(request, 'home/unit_detail.html', context)

@login_required(login_url="/login/")
def task_list(request):
    query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    location_filter = request.GET.get('location', '')
    tasks = Task.objects.all()

    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if location_filter:
        tasks = tasks.filter(location__name__icontains=location_filter)

    open_tasks = tasks.filter(status='open')
    assigned_tasks = tasks.filter(assigned_to=request.user)
    closed_tasks = tasks.filter(status='closed')
    locations = Location.objects.all()

    context = {
        'open_tasks': open_tasks,
        'assigned_tasks': assigned_tasks,
        'closed_tasks': closed_tasks,
        'query': query,
        'status_filter': status_filter,
        'location_filter': location_filter,
        'locations': locations,
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


def create_quick_task(request):
    if request.method == 'POST':
        form = QuickTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.status = 'open'
            task.save()
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

def other_hub(request):
    # Set default project_type to 'construction'
    project_type = request.GET.get('project_type', 'other')
    
    # Filter projects by the specified or default project type
    projects = Project.objects.filter(project_type=project_type)

    if request.method == 'POST':
        if 'document' in request.FILES:
            project_id = request.POST.get('project_id')
            try:
                project = get_object_or_404(Project, pk=project_id)
            except Project.DoesNotExist:
                return render(request, 'home/OtherProjects.html', {'error': 'Project not found', 'projects': projects})
            file = request.FILES['document']
            is_model = request.POST.get('is_model', 'off') == 'on'
            ProjectDocument.objects.create(project=project, file=file, is_model=is_model)
            return HttpResponseRedirect(reverse('other_hub') + f'?project_type={project_type}')
        elif 'file' in request.FILES:
            form = ReferenceMaterialForm(request.POST, request.FILES)
            if form.is_valid():
                reference_material = form.save(commit=False)
                project_id = form.cleaned_data['project'].id
                reference_material.project = get_object_or_404(Project, pk=project_id)
                reference_material.save()
                return HttpResponseRedirect(reverse('other_hub') + f'?project_type={project_type}')
            else:
                return render(request, 'home/OtherProjects.html', {'error': 'Invalid form submission', 'projects': projects})

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

    return render(request, 'home/OtherProjects.html', {
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

def budget_accounting_hub(request):
    projects = Project.objects.all()
    return render(request, 'home/budget_accounting.html', {'projects': projects})

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