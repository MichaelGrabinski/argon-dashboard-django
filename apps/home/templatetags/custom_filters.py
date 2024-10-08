from django import template

register = template.Library()

@register.filter(name='endswith')
def endswith(value, arg):
    return str(value).endswith(arg)

@register.filter
def parent_title(task):
    return task.parent_task.title if task.parent_task else ''
    
@register.filter
def parent_id(task):
    return task.parent_task.id if task.parent_task else 0