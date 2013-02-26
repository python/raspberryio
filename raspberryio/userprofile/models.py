from django.db import models

from raspberryio.aggregator.models import Feed


class Profile(models.Model):
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
                               help_text="Upload an image no larger than 500x500px and 1MB.")

    def clean(self):
        # strip twitter_id of @ symbol, if present
        if self.twitter_id.startswith('@'):
            self.twitter_id = self.twitter_id.lstrip('@')

    def __unicode__(self):
        return self.user.username

    @models.permalink
    def get_absolute_url(self):
        return ('profile', (self.user.username,))

    @property
    def feed_owner(self):
        "Determine if Profile.user manages feeds"
        return True if Feed.objects.filter(owner=self.user) else False
