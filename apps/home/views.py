# -*- encoding: utf-8 -*-
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .forms import ToolSearchForm
from apps.home.models import Tool, MaintenanceRecord, Property, Floor, Unit


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


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
    print("View executed")  # Debug print statement
    tools = Tool.objects.all()  # Fetch all tools without filtering
    records = MaintenanceRecord.objects.all()  # Fetch all maintenance records
    print(f"Tools count: {tools.count()}")  # Print the count of tools
    print(f"Records count: {records.count()}")  # Print the count of records
    for tool in tools:
        print(f"Tool: {tool.name}, Location: {tool.location}")  # Print each tool's details
    for record in records:
        print(f"Record: {record.tool.name} - {record.date}, Description: {record.description}, Performed by: {record.performed_by}")  # Print each maintenance record's details
    context = {
        'form': ToolSearchForm(),
        'tools': tools,
        'records': records,
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
    
    
def properties_list(request):
    properties = Property.objects.all()
    context = {
        'properties': properties,
    }
    return render(request, 'home/properties_list.html', context)

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    floors = property.floors.all()
    context = {
        'property': property,
        'floors': floors,
    }
    return render(request, 'home/property_detail.html', context)

def floor_detail(request, property_pk, floor_pk):
    property = get_object_or_404(Property, pk=property_pk)
    floor = get_object_or_404(Floor, pk=floor_pk, property=property)
    units = floor.units.all()
    context = {
        'property': property,
        'floor': floor,
        'units': units,
    }
    return render(request, 'home/floor_detail.html', context)

def unit_detail(request, property_pk, floor_pk, unit_pk):
    property = get_object_or_404(Property, pk=property_pk)
    floor = get_object_or_404(Floor, pk=floor_pk, property=property)
    unit = get_object_or_404(Unit, pk=unit_pk, floor=floor)
    images = unit.images.all()
    open_repairs = unit.open_repairs.all()
    maintenance_logs = unit.maintenance_logs.all()
    rent_payments = unit.rent_payments.all()
    context = {
        'property': property,
        'floor': floor,
        'unit': unit,
        'images': images,
        'open_repairs': open_repairs,
        'maintenance_logs': maintenance_logs,
        'rent_payments': rent_payments,
    }
    return render(request, 'home/unit_detail.html', context)