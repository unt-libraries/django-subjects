import markdown as mkdn

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdown(value):
    return mark_safe(mkdn.markdown(value, safe_mode='escape'))
