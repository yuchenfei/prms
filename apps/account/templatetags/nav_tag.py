from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def nav_class(context, *args):
    for arg in args:
        if arg:
            # print(reverse(arg))
            # print(context.request.path)
            if reverse(arg) == context.request.path:
                return 'active'
    return ""
