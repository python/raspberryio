from django.contrib.auth.models import User
from django.db import models

from raspberryio.search.models import Searchable


class SearchableUser(Searchable, User):
    """
    A proxy model on django.contrib.auth.models.User to make user fields
    searchable.
    """

    search_fields = {
        'username': 10, 'first_name': 10, 'last_name': 5
    }

    class Meta(object):
        proxy = True


class Profile(Searchable):
    """
    The user profile model
    """

    user = models.OneToOneField("auth.User")
    bio = models.TextField(blank=True, default='')
    website = models.URLField(blank=True, default='')
    twitter_id = models.CharField(max_length=200, blank=True, default='')
    use_gravatar = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to="images/avatars",
                               blank=True, null=True,
                               help_text="Upload an avatar")

    search_fields = {'bio': 5, 'twitter_id': 10}

    def clean(self):
        # strip twitter_id of @ symbol, if present
        if self.twitter_id.startswith('@'):
            self.twitter_id = self.twitter_id.lstrip('@')

    def __unicode__(self):
        return self.user.username

    @models.permalink
    def get_absolute_url(self):
        return ('profile', (self.user.username,))
