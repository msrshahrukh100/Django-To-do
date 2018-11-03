from django import template
from django.utils.dateparse import parse_datetime

register = template.Library()


@register.filter(name='converttodate')
def converttodate(value):
    return parse_datetime(value)