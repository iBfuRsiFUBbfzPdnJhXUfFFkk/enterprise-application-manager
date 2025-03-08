from django import template

register = template.Library()


@register.filter(name="get_color")
def get_color(value):
    try:
        value = float(value)
    except (ValueError, TypeError):
        return "#F44336"
    if value >= 1.0:
        return "#4CAF50"
    elif value >= 0.9:
        return "#8BC34A"
    elif value >= 0.8:
        return "#CDDC39"
    elif value >= 0.7:
        return "#FFC107"
    elif value >= 0.6:
        return "#FF9800"
    elif value >= 0.5:
        return "#FF5722"
    elif value >= 0.4:
        return "#FF7043"
    else:
        return "#F44336"
