from django import template

register = template.Library()

@register.filter(name='split')
def split(value, delimiter=','):
    """
    Returns the string split by delimiter.
    Example: {{ value|split:"," }}
    """
    return value.split(delimiter) 

@register.filter
def get_item(dictionary, key):
    """Gets an item from a dictionary using bracket notation"""
    return dictionary.get(key)

@register.filter(name='trim')
def trim(value):
    """Trims leading and trailing whitespace from a string."""
    if isinstance(value, str):
        return value.strip()
    return value
