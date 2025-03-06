from django import template

register = template.Library()


@register.filter(name="get_color")
def get_color(value):
    """
    Returns a color code based on the given value.
    Every 0.1 increment changes the shade, starting from 0.4.
    """
    try:
        value = float(value)
    except (ValueError, TypeError):
        return "#F44336"  # Default to red for invalid values

    if value >= 1.0:
        return "#4CAF50"  # Green
    elif value >= 0.9:
        return "#8BC34A"  # Light Green
    elif value >= 0.8:
        return "#CDDC39"  # Lime
    elif value >= 0.7:
        return "#FFC107"  # Amber
    elif value >= 0.6:
        return "#FF9800"  # Orange
    elif value >= 0.5:
        return "#FF5722"  # Deep Orange
    elif value >= 0.4:
        return "#FF7043"  # Lighter Red-Orange
    else:
        return "#F44336"  # Red
