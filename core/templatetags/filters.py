from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='marksafe')
def marksafe(val):
    return mark_safe(val)

@register.filter(name='type')
def marksafe(val):
    return type(val)


