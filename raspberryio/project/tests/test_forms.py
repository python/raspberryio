from django.test.client import RequestFactory

from raspberryio.project.tests.base import ProjectBaseTestCase
from raspberryio.project.forms import ProjectImageForm, ProjectStepForm


class ProjectFormTestCase(ProjectBaseTestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.project = self.create_project()

    def test_placeholder_labels(self):
        request = self.request_factory.get('/')
        form = ProjectStepForm()
        # first assert that label is shown
        self.assertEqual(form.fields['title'].label, 'Title')
        form.Meta.remove_labels = True
        form = ProjectStepForm(request.GET, instance=self.project)
        # now assert that Meta attribute removes it
        self.assertEqual(form.fields['title'].label, '')

class ProjectStepFormTestCase(ProjectBaseTestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.project = self.create_project()
        self.project_step = self.create_project_step(project=self.project)

    def test_no_content(self):
        request = self.request_factory.post('/', {})
        form = ProjectStepForm(request.POST, instance=self.project_step)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['content'], ['This field is required.'])

    def test_images_empty(self):
        post_data = {
            'title': self.get_random_string(),
            'content': self.get_random_string(),
            'images': []
        }
        request = self.request_factory.post('/', post_data)
        form = ProjectStepForm(request.POST, instance=self.project_step)
        if form.is_valid():
            project_step = form.save()
            self.assertEqual(project_step.gallery.count(), 0)
        else:
            self.fail('Form should be valid')

    def test_images_bad_format(self):
        self.create_project_image()
        post_data = {
            'title': self.get_random_string(),
            'content': self.get_random_string(),
            'images': ['not']
        }
        request = self.request_factory.post('/', post_data)
        form = ProjectStepForm(request.POST, instance=self.project_step)
        if form.is_valid():
            project_step = form.save()
            self.assertEqual(list(project_step.gallery.all()), [])
        else:
            self.fail('Form should be valid')

    def test_images_bad_ids(self):
        self.create_project_image()
        post_data = {
            'title': self.get_random_string(),
            'content': self.get_random_string(),
            'images': ['99,100']
        }
        request = self.request_factory.post('/', post_data)
        form = ProjectStepForm(request.POST, instance=self.project_step)
        if form.is_valid():
            project_step = form.save()
            self.assertEqual(list(project_step.gallery.all()), [])
        else:
            self.fail('Form should be valid')

    def test_images_valid(self):
        project_image = self.create_project_image()
        post_data = {
            'title': self.get_random_string(),
            'content': self.get_random_string(),
            'images': [str(project_image.id)]
        }
        request = self.request_factory.post('/', post_data)
        form = ProjectStepForm(request.POST, instance=self.project_step)
        if form.is_valid():
            project_step = form.save()
            self.assertEqual(list(project_step.gallery.all()), [project_image])
        else:
            self.fail('Form should be valid')

    def test_multiple_images_valid(self):
        project_image1 = self.create_project_image()
        project_image2 = self.create_project_image()
        project_images = (project_image1, project_image2)
        post_data = {
            'title': self.get_random_string(),
            'content': self.get_random_string(),
            'images': ','.join([str(image.id) for image in project_images])
        }
        request = self.request_factory.post('/', post_data)
        form = ProjectStepForm(request.POST, instance=self.project_step)
        if form.is_valid():
            project_step = form.save()
            self.assertEqual(tuple(project_step.gallery.all()), project_images)
        else:
            self.fail('Form should be valid')

    def test_bad_video_url(self):
        post_data = {
            'title': self.get_random_string(),
            'content': self.get_random_string(),
            'video': 'http://example.com/badurl',
        }
        request = self.request_factory.post('/', post_data)
        form = ProjectStepForm(request.POST, instance=self.project_step)
        self.assertFalse(form.is_valid())


class ProjectImageFormTestCase(ProjectBaseTestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.project = self.create_project()

    def test_valid_file_upload(self):
        filename = self.get_random_string()
        f = self.create_file(filename=filename)
        request = self.request_factory.post('/', {'file': f})
        request.is_ajax = True
        form = ProjectImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            self.assertEqual(instance.get_filename(), filename)
        else:
            self.fail('Form should be valid')

    def test_invalid_upload(self):
        request = self.request_factory.post('/', {'filez': self.create_file()})
        request.is_ajax = True
        form = ProjectImageForm(request.POST or None, request.FILES or None)
        self.assertFalse(form.is_valid())

    def test_no_file(self):
        request = self.request_factory.post('/', {})
        request.is_ajax = True
        form = ProjectImageForm(request.POST or None, request.FILES or None)
        self.assertFalse(form.is_valid())
