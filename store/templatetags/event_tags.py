from django import template

register = template.Library()

@register.filter(name='abs')
def convert_abs(value):
    return (-1*value)