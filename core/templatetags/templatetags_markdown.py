from django import template
from django.utils.safestring import mark_safe
from markdown import markdown

register = template.Library()


@register.filter(name='markdown')
def markdown_filter(value: str | None) -> str:
    if value is None:
        return ""
    return mark_safe(s=markdown(text=value))


@register.filter(name='split')
def split_filter(value: str | None, delimiter: str = ',') -> list:
    """Split a string by the given delimiter."""
    if value is None:
        return []
    return value.split(delimiter)


@register.filter(name='trim')
def trim_filter(value: str | None) -> str:
    """Trim whitespace from a string."""
    if value is None:
        return ""
    return value.strip()
