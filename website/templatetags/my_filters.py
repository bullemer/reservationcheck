from django import template
from datetime import datetime
from datetime import date

register = template.Library()

@register.filter
def days_until(value):
    if not isinstance(value, date):
        return
    now = datetime.now().date()  # Convert datetime to date
    return (value - now).days