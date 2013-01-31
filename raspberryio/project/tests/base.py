from django.contrib.sites.models import Site as DjangoSite

from hilbert.test import TestCase
from mezzanine.utils.sites import current_site_id

from raspberryio.userprofile import models as userprofile
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
        user.save()
        return user

    def create_user_profile(self, user=None, **kwargs):
        user = user or self.create_user()
        return self.create_instance(userprofile.Profile, user=user, **kwargs)

    def get_current_site(self):
        return DjangoSite.objects.get(id=current_site_id())


class ProjectBaseTestCase(RaspberryIOBaseTestCase):

    def create_project(self, **kwargs):
        defaults = {
            'title': self.get_random_string(length=500),
            'site': kwargs.pop('site', self.create_site()),
            'user': kwargs.pop('user', self.create_user()),
        }
        return self.create_instance(
            project.Project, defaults=defaults, **kwargs
        )

    def create_project_step(self, **kwargs):
        defaults = {
            'project': kwargs.pop('project', self.create_project()),
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
