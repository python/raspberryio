from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect

from actstream import models

from raspberryio.userprofile.models import Profile


def profile_related_list(request, username, relation):
    "Render the list of a users folllowers or who the user is following"
    profile = get_object_or_404(Profile, user__username__iexact=username)
    if profile.user.username != username:
        return redirect(profile, permanent=True)
    user = profile.user

    # get a queryset of users described by this relationship
    if relation == 'followers':
        related_users = models.followers(user)
    elif relation == 'following':
        related_users = models.following(user)
    return render(request, "accounts/account_profile_related.html", {
        'user': user,
        'profile': profile,
        'related_users': related_users,
    })


def profile_actions(request, username):
    "Custom renderer for user profile activity stream"
    profile = get_object_or_404(Profile, user__username__iexact=username)
    if profile.user.username != username:
        return redirect(profile, permanent=True)
    user = profile.user
    return render(request, "accounts/account_profile_actions.html", {
        'user': user,
        'profile': profile,
        'actions': models.actor_stream(user),
    })


@login_required
def profile_dashboard(request):
    """
    Landing page for logged in users. Renders the activity stream of followed
    users.
    """
    user = get_object_or_404(User, id=request.user.id)
    return render(request, "accounts/account_dashboard.html", {
        'user': user,
        'profile': user.get_profile(),
        'actions': models.user_stream(user),
    })


def profile_users(request):
    """Returns the list of active site users"""
    users = User.objects.filter(is_active=True).order_by('username')
    paginator = Paginator(users, 20)

    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)
    return render(request, "accounts/activeusers.html", {
        'users': users
    })
