from raspberryio.project.tests.base import ProjectBaseTestCase
from django.test.client import RequestFactory
from django.conf import settings

class ProjectStepTestCase(ProjectBaseTestCase):

    def setUp(self):
        self.user = self.create_user()
        self.project = self.create_project(user=self.user)
        self.request_factory = RequestFactory()

    def test_is_editable_project_user(self):
        request = self.request_factory.get('/')
        request.user = self.project.user
        self.assertTrue(
            self.project.is_editable(request),
            'A user should be able to edit the project steps of their own project',
        )

    def test_is_editable_not_project_user(self):
        request = self.request_factory.get('/')
        request.user = self.create_user()
        self.assertFalse(
            self.project.is_editable(request),
            "A user should not be able to edit the project steps of another user's project",
        )

    def test_is_editable_superuser(self):
        request = self.request_factory.get('/')
        request.user = self.create_superuser()
        self.assertTrue(
            self.project.is_editable(request),
            'Superusers should be able to edit any project step',
        )
