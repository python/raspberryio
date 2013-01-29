from datetime import timedelta

from django.core.urlresolvers import reverse

from hilbert.test import ViewTestMixin, AuthViewMixin
from mezzanine.utils.timezone import now
from mezzanine.core.models import (CONTENT_STATUS_PUBLISHED,
    CONTENT_STATUS_DRAFT)
from mezzanine.blog.models import BlogCategory

from raspberryio.project.tests.base import ProjectBaseTestCase


class ProjectDetailViewTestCase(ViewTestMixin, ProjectBaseTestCase):
    url_name = 'project-detail'

    def setUp(self):
        self.user = self.create_user(data={'password': 'password'})
        self.project = self.create_project(
            user=self.user, status=CONTENT_STATUS_PUBLISHED
        )
        super(ProjectDetailViewTestCase, self).setUp()

    def get_url_args(self):
        return (self.project.slug,)

    def test_draft_hidden_other_user(self):
        other_user = self.create_user(data={'password': 'password'})
        # Project status is draft
        self.project.status = CONTENT_STATUS_DRAFT
        self.project.save()
        self.client.login(username=other_user.username, password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
        # Project status is published, but publish_date is in the future
        self.project.status = CONTENT_STATUS_PUBLISHED
        self.project.publish_date = now() + timedelta(minutes=1)
        self.project.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_draft_visible_projectuser(self):
        # Project status is draft
        self.project.status = CONTENT_STATUS_DRAFT
        self.project.save()
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Project status is published, but publish_date is in the future
        self.project.status = CONTENT_STATUS_PUBLISHED
        self.project.publish_date = now() + timedelta(minutes=1)
        self.project.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_draft_visible_superuser(self):
        super_user = self.create_superuser(data={'password': 'password'})
        # Project status is draft
        self.project.status = CONTENT_STATUS_DRAFT
        self.project.save()
        self.client.login(username=super_user.username, password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Project status is published, but publish_date is in the future
        self.project.status = CONTENT_STATUS_PUBLISHED
        self.project.publish_date = now() + timedelta(minutes=1)
        self.project.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_bad_slug(self):
        response = self.client.get(reverse(self.url_name, args=['bad-slug']))
        self.assertEqual(response.status_code, 404)


class ProjectListViewTestCase(ViewTestMixin, ProjectBaseTestCase):
    url_name = 'project-list'

    def setUp(self):
        self.user = self.create_user(data={'password': 'password'})
        self.project = self.create_project(
            user=self.user, status=CONTENT_STATUS_PUBLISHED
        )
        super(ProjectListViewTestCase, self).setUp()

    def test_hide_unpublished(self):
        self.client.login(username=self.user.username, password='password')
        self.project.status = CONTENT_STATUS_DRAFT
        self.project.save()
        response = self.client.get(self.url)
        projects = response.context['projects']
        self.assertQuerysetEqual(projects, [])

    def test_show_unpublished_to_superusers(self):
        super_user = self.create_superuser(data={'password': 'password'})
        self.client.login(username=super_user.username, password='password')
        self.project.status = CONTENT_STATUS_DRAFT
        self.project.save()
        response = self.client.get(self.url)
        projects = response.context['projects']
        self.assertEquals(list(projects), [self.project])


class ProjectCreateEditTestCase(AuthViewMixin, ProjectBaseTestCase):
    url_name = 'project-create-edit'

    def setUp(self):
        super(ProjectCreateEditTestCase, self).setUp()
        self.project = self.create_project(
            user=self.user, status=CONTENT_STATUS_PUBLISHED
        )

    def get_edit_url(self, project_slug=''):
        """
        self.url points to using the view for creating a new project. Use
        this helper to create a link to the edit view.
        """
        return reverse(
            self.url_name, args=(project_slug or self.project.slug,)
        )

    def test_other_user_cannot_edit(self):
        other_user = self.create_user(data={'password': 'password'})
        self.client.login(username=other_user.username, password='password')
        url = self.get_edit_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_edit(self):
        super_user = self.create_superuser(data={'password': 'password'})
        self.client.login(username=super_user.username, password='password')
        url = self.get_edit_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_bad_slug(self):
        url = self.get_edit_url('bad-slug')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_valid(self):
        category, created = BlogCategory.objects.get_or_create(title='foo')
        form_data = {
            'title': self.get_random_string(),
            'tldr': self.get_random_string(),
            'status': CONTENT_STATUS_DRAFT,
            'categories': [category.id]
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)

    def test_create_invalid(self):
        response = self.client.post(self.url, {'title': ''})
        project_form = response.context['project_form']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(project_form.errors)

    def test_edit_valid_form(self):
        form_data = {
            'title': self.get_random_string(),
            'tldr': self.get_random_string(),
            'status': CONTENT_STATUS_DRAFT,
            'categories': [self.create_category().id]
        }
        response = self.client.post(self.get_edit_url(), form_data)
        self.assertEqual(response.status_code, 302)

    def test_edit_invalid_form(self):
        response = self.client.post(self.url, {'title': ''})
        project_form = response.context['project_form']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(project_form.errors)

    def test_edit_form_wrong_user(self):
        other_user = self.create_user(data={'password': 'password'})
        self.client.login(username=other_user.username, password='password')
        form_data = {
            'title': self.get_random_string(),
            'tldr': self.get_random_string(),
            'status': CONTENT_STATUS_DRAFT,
            'categories': [self.create_category().id]
        }
        response = self.client.post(self.get_edit_url(), form_data)
        self.assertEqual(response.status_code, 403)
