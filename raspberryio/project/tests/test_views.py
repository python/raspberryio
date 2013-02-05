from datetime import timedelta

from django.core.urlresolvers import reverse

from hilbert.test import ViewTestMixin, AuthViewMixin
from mezzanine.utils.timezone import now
from mezzanine.core.models import (CONTENT_STATUS_PUBLISHED,
    CONTENT_STATUS_DRAFT)

from raspberryio.project.tests.base import ProjectBaseTestCase
from raspberryio.project.models import Project


class ProjectDetailViewTestCase(ViewTestMixin, ProjectBaseTestCase):
    url_name = 'project-detail'

    def setUp(self):
        self.user = self.create_user(data={'password': 'password'})
        self.project = self.create_project(user=self.user)
        # Status is set to DRAFT on first save. Needs to be published for the
        # detail view to display the project.
        self.project.status = CONTENT_STATUS_PUBLISHED
        self.project.save()
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
        form_data = {
            'title': 'new-project',
            'tldr': self.get_random_string(),
            'categories': [self.create_project_category().id],
            'save': 'value',
        }
        response = self.client.post(self.url, form_data, follow=True)
        new_project = Project.objects.get(slug='new-project')
        url, status_code = response.redirect_chain[0]
        expected_url = reverse(
            'project-detail', args=[new_project.slug]
        )
        self.assertEqual(status_code, 302)
        self.assertTrue(expected_url in url,
            "Didn't redirect to {0}, redirected to {1}".format(expected_url, url)
        )

    def test_create_valid_and_add_steps(self):
        form_data = {
            'title': 'new-project',
            'tldr': self.get_random_string(),
            'categories': [self.create_project_category().id],
            'save-add-step': 'value',
        }
        response = self.client.post(self.url, form_data, follow=True)
        new_project = Project.objects.get(slug='new-project')
        url, status_code = response.redirect_chain[0]
        expected_url = reverse(
            'project-step-create-edit', args=[new_project.slug]
        )
        self.assertEqual(status_code, 302)
        self.assertTrue(expected_url in url,
            "Didn't redirect to {0}, redirected to {1}".format(expected_url, url)
        )

    def test_create_invalid(self):
        response = self.client.post(self.url, {'title': ''})
        project_form = response.context['project_form']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(project_form.errors)

    def test_edit_valid_form(self):
        form_data = {
            'title': 'current-project',
            'tldr': self.get_random_string(),
            'categories': [self.create_project_category().id]
        }
        response = self.client.post(self.get_edit_url(), form_data, follow=True)
        current_project = Project.objects.get(title='current-project')
        url, status_code = response.redirect_chain[0]
        expected_url = reverse('project-detail', args=[current_project.slug])
        self.assertEqual(status_code, 302)
        self.assertTrue(expected_url in url,
            "Didn't redirect to {0}, redirected to {1}".format(expected_url, url)
        )

    def test_edit_invalid_form(self):
        response = self.client.post(self.get_edit_url(), {'title': ''})
        project_form = response.context['project_form']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(project_form.errors)

    def test_edit_form_wrong_user(self):
        other_user = self.create_user(data={'password': 'password'})
        self.client.login(username=other_user.username, password='password')
        form_data = {
            'title': self.get_random_string(),
            'tldr': self.get_random_string(),
            'categories': [self.create_project_category().id]
        }
        response = self.client.post(self.get_edit_url(), form_data)
        self.assertEqual(response.status_code, 403)


class ProjectStepCreateEditTestCase(AuthViewMixin, ProjectBaseTestCase):
    url_name = 'project-step-create-edit'

    def setUp(self):
        self.project = self.create_project(status=CONTENT_STATUS_PUBLISHED)
        super(ProjectStepCreateEditTestCase, self).setUp()
        # AuthViews create and auto-login a user. Set the project to belong to
        # this user
        self.project.user = self.user
        self.project.save()

    def get_url_args(self):
        """ Sets the args for the create project step url set in self.url """
        return (self.project.slug,)

    def get_edit_url(self, project_slug, step_order):
        """
        self.url points to using the view for creating a new step. Use this
        helper to create a link to the edit view.
        """
        return reverse(self.url_name, args=(project_slug, step_order))

    def test_other_user_cannot_edit(self):
        other_user = self.create_user(data={'password': 'password'})
        self.client.login(username=other_user.username, password='password')
        project_step = self.create_project_step(project=self.project)
        url = self.get_edit_url(self.project.slug, project_step._order)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_edit(self):
        super_user = self.create_superuser(data={'password': 'password'})
        self.client.login(username=super_user.username, password='password')
        project_step = self.create_project_step(project=self.project)
        url = self.get_edit_url(self.project.slug, project_step._order)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_bad_project_slug(self):
        project_step = self.create_project_step(project=self.project)
        url = self.get_edit_url('bad-slug', project_step._order)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_bad_order_number(self):
        project_step = self.create_project_step(project=self.project)
        url = self.get_edit_url(self.project.slug, 4)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_valid(self):
        form_data = {
            'content': self.get_random_string(),
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)

    def test_create_invalid(self):
        response = self.client.post(self.url, {'content': ''})
        project_step_form = response.context['project_step_form']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(project_step_form.errors)

    def test_edit_valid_form(self):
        form_data = {
            'content': self.get_random_string(),
        }
        project_step = self.create_project_step(project=self.project)
        edit_url = self.get_edit_url(self.project.slug, project_step._order)
        response = self.client.post(edit_url, form_data, follow=True)
        url, status_code = response.redirect_chain[0]
        expected_url = reverse('project-detail', args=[self.project.slug])
        self.assertEqual(status_code, 302)
        self.assertTrue(expected_url in url,
            "Didn't redirect to {0}, redirected to {1}".format(expected_url, url)
        )

    def test_edit_invalid_form(self):
        project_step = self.create_project_step(project=self.project)
        edit_url = self.get_edit_url(self.project.slug, project_step._order)
        response = self.client.post(edit_url, {'content': ''})
        project_step_form = response.context['project_step_form']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(project_step_form.errors)

    def test_edit_form_wrong_user(self):
        other_user = self.create_user(data={'password': 'password'})
        self.client.login(username=other_user.username, password='password')
        form_data = {
            'content': self.get_random_string(),
        }
        project_step = self.create_project_step(project=self.project)
        edit_url = self.get_edit_url(self.project.slug, project_step._order)
        response = self.client.post(edit_url, form_data)
        self.assertEqual(response.status_code, 403)

    def test_add_another_redirect(self):
        form_data = {
            'content': self.get_random_string(),
            'save-add': 'Anything',
        }
        project_step = self.create_project_step(project=self.project)
        edit_url = self.get_edit_url(self.project.slug, project_step._order)
        response = self.client.post(edit_url, form_data, follow=True)
        url, status_code = response.redirect_chain[0]
        expected_url = reverse(
            'project-step-create-edit', args=[self.project.slug]
        )
        self.assertEqual(status_code, 302)
        self.assertTrue(expected_url in url,
            "Didn't redirect to {0}, redirected to {1}".format(expected_url, url)
        )


class ProjectDetailViewTestCase(ProjectBaseTestCase):
    url_name = 'publish-project'

    def setUp(self):
        self.user = self.create_user(data={'password': 'password'})
        self.project = self.create_project(user=self.user)
        self.url = reverse('publish-project', args=(self.project.slug,))

    def test_valid_publish(self):
        self.client.login(username=self.user.username, password='password')
        self.assertEqual(self.project.status, CONTENT_STATUS_DRAFT)
        response = self.client.post(self.url, {}, is_ajax=True)
        project = Project.objects.get(slug=self.project.slug)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(project.status, CONTENT_STATUS_PUBLISHED)

    def test_reject_non_project_user(self):
        other_user = self.create_user(data={'password': 'password'})
        self.client.login(username=other_user.username, password='password')
        self.assertEqual(self.project.status, CONTENT_STATUS_DRAFT)
        response = self.client.post(self.url, {}, is_ajax=True)
        project = Project.objects.get(slug=self.project.slug)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(project.status, CONTENT_STATUS_DRAFT)

    def test_superuser_valid(self):
        superuser = self.create_superuser({'password': 'password'})
        self.client.login(username=superuser.username, password='password')
        self.assertEqual(self.project.status, CONTENT_STATUS_DRAFT)
        response = self.client.post(self.url, {}, is_ajax=True)
        project = Project.objects.get(slug=self.project.slug)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(project.status, CONTENT_STATUS_PUBLISHED)

    def test_invalid_slug(self):
        self.client.login(username=self.user.username, password='password')
        self.assertEqual(self.project.status, CONTENT_STATUS_DRAFT)
        url = reverse(self.url_name, args=('bad-project-slug',))
        response = self.client.post(url, {}, is_ajax=True)
        project = Project.objects.get(slug=self.project.slug)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(project.status, CONTENT_STATUS_DRAFT)
