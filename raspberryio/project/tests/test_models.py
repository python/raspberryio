from datetime import timedelta

from django.test.client import RequestFactory

from mezzanine.utils.timezone import now
from mezzanine.core.models import (CONTENT_STATUS_PUBLISHED,
    CONTENT_STATUS_DRAFT)

from raspberryio.project.tests.base import ProjectBaseTestCase


class ProjectTestCase(ProjectBaseTestCase):

    def setUp(self):
        self.project = self.create_project()

    def test_is_published(self):
        self.project.status = CONTENT_STATUS_PUBLISHED
        self.project.save()
        self.assertTrue(self.project.is_published,
            'Should return True since the default publish_date is past and the status is "Published"'
        )

    def test_is_published_false(self):
        self.project.publish_date = now() + timedelta(minutes=1)
        self.project.save()
        self.assertFalse(self.project.is_published,
            'Should return False if publish_date is in the future'
        )
        self.project.publish_date = now() - timedelta(minutes=1)
        self.project.status = CONTENT_STATUS_DRAFT
        self.project.save()
        self.assertFalse(self.project.is_published,
            'Should return False if status is "Draft"'
        )
        self.project_publish_date = now() + timedelta(minutes=1)
        self.project.save()
        self.assertFalse(self.project.is_published,
            'Should return False if status is "Draft" and publish_date is in the future'
        )


class ProjectStepTestCase(ProjectBaseTestCase):

    def setUp(self):
        self.user = self.create_user()
        self.project = self.create_project(user=self.user)
        self.project_step = self.create_project_step(project=self.project)
        self.request_factory = RequestFactory()

    def test_is_editable_project_user(self):
        request = self.request_factory.get('/')
        request.user = self.project.user
        self.assertTrue(
            self.project_step.is_editable(request),
            'A user should be able to edit the project steps of their own project',
        )

    def test_is_editable_not_project_user(self):
        request = self.request_factory.get('/')
        request.user = self.create_user()
        self.assertFalse(
            self.project_step.is_editable(request),
            "A user should not be able to edit the project steps of another user's project",
        )

    def test_is_editable_superuser(self):
        request = self.request_factory.get('/')
        request.user = self.create_superuser()
        self.assertTrue(
            self.project_step.is_editable(request),
            'Superusers should be able to edit any project step',
        )
