from urllib.parse import urlencode
from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def fix_pagination(context, **kwargs):

    query = context.get('request').GET.copy()
    query.update(kwargs)
    return urlencode(query)
