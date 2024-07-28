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
from apps.home.models import Task, Attachment, Comment, ActivityLog
from .forms import TaskForm, CommentForm, AttachmentForm, AssignTaskForm, QuickTaskForm
from django.contrib.auth.models import User
from django import forms

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task, Tool, MaintenanceRecord

@login_required(login_url="/login/")
def index(request):
    total_open_tickets = Task.objects.filter(status='open').count()
    tickets_assigned_to_you = Task.objects.filter(assigned_to=request.user).count()
    total_tools = Tool.objects.count()
    total_maintenance_records = MaintenanceRecord.objects.count()
    total_users = User.objects.count()

    context = {
        'segment': 'index',
        'total_open_tickets': total_open_tickets,
        'tickets_assigned_to_you': tickets_assigned_to_you,
        'total_tools': total_tools,
        'total_maintenance_records': total_maintenance_records,
        'total_users': total_users,
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
       open_tickets = Task.objects.filter(location__name=unit.unit_number, status='open')
       
       # Debugging print statement
       print(f"Open Tickets: {open_tickets}")

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