from django import template

register = template.Library()


@register.filter
def times(number):
    """Return a range(number) so templates can loop `number` times.

    Usage: {% for _ in rating|times %}★{% endfor %}
    """
    try:
        return range(int(number))
    except (TypeError, ValueError):
        return range(0)


@register.filter
def subtract_from_five(number):
    """Return range(5 - number), used to render empty stars after filled ones."""
    try:
        return range(max(0, 5 - int(number)))
    except (TypeError, ValueError):
        return range(0)
