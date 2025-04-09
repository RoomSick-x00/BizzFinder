from django import template

register = template.Library()

@register.filter(name='split')
def split(value, delimiter=','):
    """
    Returns the string split by delimiter.
    Example: {{ value|split:"," }}
    """
    return value.split(delimiter) 