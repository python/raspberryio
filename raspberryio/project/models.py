from django.db import models

from mezzanine.core.models import Displayable, Ownable, Orderable, RichText
from mezzanine.core.fields import RichTextField
from mezzanine.utils.models import AdminThumbMixin, upload_to
from mezzanine.utils.timezone import now
from mezzanine.galleries.models import Gallery
from mezzanine.blog.models import BlogCategory


class Project(Displayable, Ownable, AdminThumbMixin):
    """
    A project submission
    """

    featured_photo = models.ImageField(
        upload_to='images/project_featured_photos', blank=True, null=True
    )
    featured_video = models.URLField(blank=True, default='')
    featured_video_thumbnail = models.ImageField(
        upload_to='images/project_featured_video_thumbnails',
        blank=True, null=True, editable=False
    )
    tldr = RichTextField()
    categories = models.ManyToManyField(BlogCategory, related_name='projects')
    score = models.IntegerField(default=0)
    created_datetime = models.DateTimeField('Created')
    modified_datetime = models.DateTimeField('Modified')

    admin_thumb_field = 'featured_photo'

    def save(self, *args, **kwargs):
        # Set created and modified datetimes if not provided.
        if not self.id and not 'created_datetime' in kwargs:
            self.created_datetime = now()
        if not 'modified_datetime' in kwargs:
            self.modified_datetime = now()
        super(Project, self).save(*args, **kwargs)


class ProjectStep(Orderable, RichText):
    """
    A step in the process of creating the project
    """

    project = models.ForeignKey('Project', related_name='steps')
    gallery = models.OneToOneField(Gallery, blank=True, null=True)
    video = models.URLField(blank=True, default='')

    def is_editable(self, request):
        """
        Restrict in-line editing to the owner of the project and superusers.
        """
        user = request.user
        return user.is_superuser or user.id == self.project.user_id
