import random
from django import template

register = template.Library()


@register.filter
def shuffle(values: list):
    random.shuffle(values)
    return values[:3]
