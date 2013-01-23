from django.db import models


class Profile(models.Model):
    user = models.OneToOneField("auth.User")
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    twitter_id = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(upload_to="images/avatars", blank=True, null=True)

    def clean_twitter_handle(self):
        handle = self.cleaned_data.get('twitter_handle', '')
        return handle[1:] if handle and handle[0] == '@' else handle
