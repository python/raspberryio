from django import template

register = template.Library()


@register.inclusion_tag('includes/avatar.html', takes_context=True)
def avatar(context, profile, size=150):
    context.update({
        'profile': profile,
        'profile_user': profile.user,
        'size': size,
    })
    return context
