from os.path import split as path_split
from collections import Iterable

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from mezzanine.core.models import (Displayable, Ownable, Orderable, RichText,
    CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED)
from mezzanine.core.fields import RichTextField
from mezzanine.utils.models import AdminThumbMixin
from mezzanine.utils.timezone import now
from mezzanine.blog.models import BlogCategory
from mezzanine.core.templatetags.mezzanine_tags import thumbnail

from raspberryio.project.utils import get_youtube_video_id


class Project(Displayable, Ownable, AdminThumbMixin):
    """
    A project submission
    """

    featured_photo = models.ImageField('Cover Photo',
        upload_to='images/project_featured_photos', blank=True, null=True,
        help_text='Upload an image for the home page. Suggested ' \
                  'dimensions are 1252x626px and max 5MB filesize.'
    )
    featured_video = models.URLField(blank=True, default='',
                                     help_text='Youtube Video URL')
    featured_video_thumbnail = models.ImageField(
        upload_to='images/project_featured_video_thumbnails',
        blank=True, null=True, editable=False
    )
    tldr = RichTextField('Description',
        help_text='A description of your project as a whole.'
    )
    categories = models.ManyToManyField(BlogCategory, related_name='projects')
    score = models.IntegerField(default=0)
    created_datetime = models.DateTimeField('Created')
    modified_datetime = models.DateTimeField('Modified')

    admin_thumb_field = 'featured_photo'

    def save(self, *args, **kwargs):
        # Set project as draft by default
        if not self.id:
            self.status = CONTENT_STATUS_DRAFT
        # Set created and modified datetimes if not provided.
        if not self.id:
            self.created_datetime = now()
        self.modified_datetime = now()
        super(Project, self).save(*args, **kwargs)

    def is_published(self, request=None):
        """
        Returns True/False if the Project is published for the user in the
        given request. Staff users can see any projects while regular users can
        see any of their own projects

        If no request is given, or the user is not staff and viewing another
        user's project, returns True if publish_date <= now() and status ==
        CONTENT_STATUS_PUBLISHED otherwise False.
        """
        if request is not None:
            if request.user.is_staff or request.user == self.user:
                return True
        return (self.publish_date <= now() and
            self.status == CONTENT_STATUS_PUBLISHED)

    @property
    def video_id(self):
        """Extract Video ID."""
        if self.featured_video:
            return get_youtube_video_id(self.featured_video)

    @property
    def embed_url(self):
        """HTML5 embed url."""
        if self.video_id:
            return 'http://www.youtube.com/embed/%s?wmode=transparent' % self.video_id
        return None

    @models.permalink
    def get_absolute_url(self):
        return ('project-detail', [self.slug])

    def __unicode__(self):
        return unicode(self.title)


class ProjectStep(Orderable, RichText):
    """
    A step in the process of creating the project
    """

    project = models.ForeignKey('Project', related_name='steps')
    title = models.CharField(max_length=500)
    gallery = models.ManyToManyField('ProjectImage', blank=True, null=True)
    video = models.URLField(blank=True, default='',
                            help_text='Enter a valid Youtube URL')

    search_classname = 'Project Step'

    class Meta(object):
        order_with_respect_to = 'project'

    def is_editable(self, request):
        """
        Restrict in-line editing to the owner of the project and superusers.

        N.B. This is implemented for projects in Ownable.is_editable
        """
        user = request.user
        return user.is_superuser or user.id == self.project.user_id

    @property
    def get_steps_count(self):
        return self.project.steps.count()

    @property
    def get_order_display(self):
        return self._order + 1

    @property
    def order(self):
        return self._order

    @models.permalink
    def get_absolute_url(self):
        # FIXME: Change to project_step_detail if/when implemented
        return ('project-detail', [self.project.slug])

    @property
    def video_id(self):
        """Extract Video ID."""
        if self.video:
            return get_youtube_video_id(self.video)

    @property
    def embed_url(self):
        """HTML5 embed url."""
        if self.video_id:
            return 'http://www.youtube.com/embed/%s?wmode=transparent' % self.video_id
        return None

    def __unicode__(self):
        return u'Step {0} of project {1}'.format(
            self._order, self.project.title
        )


class ProjectCategory(BlogCategory):
    class Meta(object):
        proxy = True


class ProjectImage(models.Model):
    file = models.ImageField(
        upload_to='images/project_gallery_images', editable=False
    )

    def get_filename(self):
        """The image's filename (without its path)"""
        return path_split(self.file.name)[-1] if self.file.name else ''

    def get_delete_url(self):
        """A url to handle deletion of the image and its model via AJAX"""
        return reverse('gallery-image-delete', args=(self.id,))

    def get_absolute_url(self):
        """A url that serves the image file"""
        return settings.MEDIA_URL + self.file.name.replace(' ', '_')

    def get_thumbnail_url(self):
        """
        A url that serves the thumbnail of the image (Creates one if none yet
        exists)
        """
        # FIXME: Make the parameters configurable
        return settings.MEDIA_URL + thumbnail(
            self.get_absolute_url(), 400, 200
        )

    def get_image_data(self):
        """Provide image data needed by jQuery File Upload templates"""
        return {
            'id': self.id,
            'name': self.get_filename(),
            'size': self.file.size,
            'url': self.get_absolute_url(),
            'thumbnail_url': self.get_thumbnail_url(),
            'delete_url': self.get_delete_url(),
            'delete_type': 'DELETE'
        }

    @classmethod
    def serialize(kls, images):
        """
        Given a ProjectImage or an iterable of ProjectImages, return a
        dictionary of the image(s) files data in the format:
            {'files': [
                {
                    'id': image.id,
                    'name': image.get_filename, ...
                }, ...
            ]}
        """
        files_data = [image.get_image_data() for image in images] \
            if isinstance(images, Iterable) else [images.get_image_data()]
        return {'files': files_data}


class FeaturedProject(models.Model):
    "A Project annotated for featuring on the Home Page"
    project = models.OneToOneField("project.Project")
    byline = models.CharField(max_length=50,
                help_text='A terse description to be used on the home page.'
                )
    photo = models.ImageField(upload_to='images/project_featured_photos',
                help_text='Upload an image for the home page. Suggested ' \
                          'dimensions are 1252x626px and max 5MB filesize.')
    featured_start_date = models.DateTimeField(default=now(),
                help_text='Date the Project will start being featured on the' \
                          'homepage.')

    class Meta:
        ordering = ['-featured_start_date']
