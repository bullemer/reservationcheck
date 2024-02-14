from django import template
from datetime import datetime

register = template.Library()

@register.filter
def days_until(value):
    now = datetime.now().date()  # Convert datetime to date
    return (value - now).days