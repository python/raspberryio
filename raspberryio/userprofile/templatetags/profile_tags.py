from django import template

register = template.Library()


@register.inclusion_tag('includes/avatar.html')
def avatar(profile, size=150):
    return {
        'profile': profile,
        'profile_user': profile.user,
        'size': size,
    }
