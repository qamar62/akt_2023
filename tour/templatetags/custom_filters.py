from django import template

register = template.Library()

@register.filter
def batch(sequence, count):
    """
    Break a sequence into lists of a specified size.
    """
    result = []
    while sequence:
        result.append(sequence[:count])
        sequence = sequence[count:]
    return result