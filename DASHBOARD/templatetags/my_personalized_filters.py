from django import template

register = template.Library()

@register.filter
def has_permission(user, perm_name):
    return user.has_perm(perm_name)