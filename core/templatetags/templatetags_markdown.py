from django import template
from django.utils.safestring import mark_safe
from markdown import markdown

register = template.Library()


@register.filter(name='markdown')
def markdown_filter(value: str | None) -> str:
    if value is None:
        return ""
    return mark_safe(s=markdown(text=value))
