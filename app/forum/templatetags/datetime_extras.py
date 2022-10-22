from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def timesince_filter(value):
    return value.split(",")[0] + " ago"
