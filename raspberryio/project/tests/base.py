from django.contrib.sites.models import Site as DjangoSite
from django.core.files.base import ContentFile

from hilbert.test import TestCase
from mezzanine.utils.sites import current_site_id

from raspberryio.project import models as project


class RaspberryIOBaseTestCase(TestCase):
    """
    Base TestCase class that provides utilities throughout the raspberryio
    project.
    """

    def create_instance(self, ModelClass, **kwargs):
        """
        Given ModelClass, validate, create and return an model instance of that
        type. Takes `defaults` as a dictionary of default values. Any
        other kwargs override the provided defaults. E.g. defaults can be
        provided in test helper methods but overriden when called, as needed:

        Example:
            create_item = create_instance(Item, default={'title': 'generic'})
            ...
            a = create_item()
            b = create_item(title='flower')
            print (a.title, b.title)
            Out: ('generic', 'flower')
        """
        defaults = kwargs.pop('defaults', {})
        defaults.update(kwargs)
        instance = ModelClass(**defaults)
        instance.clean()
        instance.save()
        return instance

    def create_site(self, **kwargs):
        defaults = {
            'name': self.get_random_string(),
            'domain': self.get_random_string(),
        }
        return self.create_instance(DjangoSite, defaults=defaults, **kwargs)

    def create_superuser(self, data=None):
        data = data or {}
        user = self.create_user(data=data)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def get_current_site(self):
        return DjangoSite.objects.get(id=current_site_id())


class ProjectBaseTestCase(RaspberryIOBaseTestCase):

    def create_project(self, **kwargs):
        defaults = {
            'title': self.get_random_string(length=500),
            'site': kwargs.pop('site', self.create_site()),
            'user': kwargs.pop('user', self.create_user()),
        }
        instance = self.create_instance(
            project.Project, defaults=defaults, **kwargs
        )
        if 'status' in kwargs:
            instance.status = kwargs['status']
            instance.save()
        return instance

    def create_project_step(self, **kwargs):
        defaults = {
            'project': kwargs.pop('project', self.create_project()),
            'title': self.get_random_string(length=500),
            'content': self.get_random_string(),
        }
        return self.create_instance(
            project.ProjectStep, defaults=defaults, **kwargs
        )

    def create_project_category(self, **kwargs):
        defaults = {
            'title': kwargs.pop('title', self.get_random_string()),
        }
        return self.create_instance(
            project.ProjectCategory, defaults=defaults, **kwargs
        )

    def create_file(self, **kwargs):
        filename = kwargs.pop('filename', 'test.jpg')
        content = kwargs.pop('content', self.get_random_string())
        temp_file = ContentFile(content)
        temp_file.name = filename
        return temp_file

    def create_project_image(self, **kwargs):
        defaults = {
            'file': kwargs.pop('file', self.create_file()),
        }
        project_step = kwargs.pop('project_step', None)
        project_image = self.create_instance(
            project.ProjectImage, defaults=defaults, **kwargs
        )
        if project_step:
            project_step.gallery.add(project_image)
        return project_image
