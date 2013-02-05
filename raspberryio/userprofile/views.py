from django.shortcuts import render, get_object_or_404, redirect

from relationships.models import RelationshipStatus
from relationships.views import get_relationship_status_or_404

from raspberryio.userprofile.models import Profile


def profile_related_list(request, username, relation=None, template="accounts/account_profile_related.html", extra_context=None):
    if not relation:
        status = RelationshipStatus.objects.following()
        relation = status.from_slug
    else:
        # get the relationship status object we're talking about
        status = get_relationship_status_or_404(relation)

    profile = get_object_or_404(Profile, user__username__iexact=username)
    if profile.user.username != username:
        return redirect(profile, permanent=True)
    user = profile.user

    # get a queryset of users described by this relationship
    if status.from_slug == relation:
        related_users = user.relationships.get_relationships(status=status)
    else:
        related_users = user.relationships.get_related_to(status=status)

    context = {
        'user': user,
        'profile': profile,
        'related_users': related_users,
    }

    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
