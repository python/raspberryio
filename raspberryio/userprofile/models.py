from django.db import models


class Profile(models.Model):
    user = models.OneToOneField("auth.User")
    bio = models.TextField(blank=True, default='')
    website = models.URLField(blank=True, default='')
    twitter_id = models.CharField(max_length=200, blank=True, default='')
    use_gravatar = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to="images/avatars",
                               blank=True, null=True,
                               help_text="Upload an avatar")

    def clean(self):
        # strip twitter_id of @ symbol, if present
        if self.twitter_id.startswith('@'):
            self.twitter_id = self.twitter_id.lstrip('@')

    def __unicode__(self):
        return self.user.username
