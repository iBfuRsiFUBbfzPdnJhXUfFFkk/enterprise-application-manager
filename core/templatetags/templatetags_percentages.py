from django import template

register = template.Library()


@register.filter(name='percentage')
def markdown_filter(
        value: str | None,
        decimals: int | None = 2,
) -> str:
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value
    return f"{value * 100:.{decimals}f}%"
