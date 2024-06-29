from django import template

register = template.Library()

@register.filter
def urlCheck(value, arg):
    return value.startswith(arg)
