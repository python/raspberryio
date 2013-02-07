from django.test.client import RequestFactory

from raspberryio.project.tests.base import ProjectBaseTestCase
from raspberryio.project.forms import ProjectImageForm


class ProjectFormTestCase(ProjectBaseTestCase):

    def setUp(self):
        self.project = self.create_project()


class ProjectStepFormTestCase(ProjectBaseTestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.project = self.create_project()
        self.project_step = self.create_project_step(project=self.project)

    def test_images_empty(self):
        pass

    def test_images_bad_format(self):
        pass

    def test_images_valid(self):

        request = self.request_factory.post('/', {'images': [1]})


class ProjectImageFormTestCase(ProjectBaseTestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.project = self.create_project()

    def test_valid_file_upload(self):
        filename = self.get_random_string()
        f = self.create_file(filename=filename)
        request = self.request_factory.post('/', {'file': f})
        request.is_ajax = True
        form = ProjectImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save()
            self.assertEqual(instance.get_filename(), filename)

    def test_no_file(self):
        request = self.request_factory.post('/', {})
        request.is_ajax = True
        form = ProjectImageForm(request.POST or None, request.FILES or None)
        self.assertFalse(form.is_valid())
