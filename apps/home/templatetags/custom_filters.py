from django import template

register = template.Library()

@register.filter(name='endswith')
def endswith(value, arg):
    return str(value).endswith(arg)