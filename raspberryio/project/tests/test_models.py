from datetime import timedelta

from django.core.urlresolvers import reverse
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
        self.assertTrue(self.project.is_published(),
            'Should return True since the default publish_date is past and the status is "Published"'
        )

    def test_is_published_false(self):
        self.project.publish_date = now() + timedelta(minutes=1)
        self.project.save()
        self.assertFalse(self.project.is_published(),
            'Should return False if publish_date is in the future'
        )
        self.project.publish_date = now() - timedelta(minutes=1)
        self.project.status = CONTENT_STATUS_DRAFT
        self.project.save()
        self.assertFalse(self.project.is_published(),
            'Should return False if status is "Draft"'
        )
        self.project_publish_date = now() + timedelta(minutes=1)
        self.project.save()
        self.assertFalse(self.project.is_published(),
            'Should return False if status is "Draft" and publish_date is in the future'
        )

    def test_default_draft(self):
        self.assertEqual(self.project.status, CONTENT_STATUS_DRAFT)

    def test_video_params(self):
        # first test that garbage input doesn't work
        self.assertEqual(self.project.embed_url, None)
        # now test a real video URL
        video_id = "6BbufUp_HNs"
        video_url = "http://www.youtube.com/watch?v=%s" % video_id
        project = self.create_project(featured_video=video_url)
        self.assertEqual(project.video_id, video_id)
        self.assertEqual(project.embed_url, 'http://www.youtube.com/embed/%s?wmode=transparent' % video_id)

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

    def test_get_steps_count_property(self):
        self.assertEqual(self.project_step.get_steps_count, 1)
        self.create_project_step(project=self.project)
        self.assertEqual(self.project_step.get_steps_count, 2)
        self.create_project_step()
        self.assertEqual(self.project_step.get_steps_count, 2,
            "step count shouldn't change when step is added to a different project"
        )

    def test_order_property(self):
        """Assure the order property provides the _order value"""
        self.assertEqual(self.project_step.order, self.project_step._order)
        project_step2 = self.create_project_step(project=self.project)
        self.assertEqual(project_step2.order, project_step2._order)

    def test_get_order_display(self):
        """Assure the get_order_display method provides the _order value + 1"""
        self.assertEqual(
            self.project_step.get_order_display, self.project_step._order + 1
        )
        project_step2 = self.create_project_step(project=self.project)
        self.assertEqual(
            project_step2.get_order_display, project_step2._order + 1
        )

    def test_order_number(self):
        """
        Assure the proper order number is assigned to new ProjectSteps. (This
        should happen from built-in Mezzanine functionality as long as
        Meta:order_with_respect_to points to the Project FK)
        """
        project2 = self.create_project(user=self.user)
        # Create two steps in each of the two projects
        project1_step0 = self.project_step
        project2_step0 = self.create_project_step(project=project2)
        project1_step1 = self.create_project_step(project=self.project)
        project2_step1 = self.create_project_step(project=project2)
        # Assure the order numbers for the steps are unique per project
        self.assertEqual(project1_step0._order, 0)
        self.assertEqual(project1_step1._order, 1)
        self.assertEqual(project2_step0._order, 0)
        self.assertEqual(project2_step1._order, 1)

    def test_absolute_url(self):
        self.assertEqual(self.project_step.get_absolute_url(),
                         reverse('project-detail', args=[self.project.slug]))

    def test_video_params(self):
        # first test that garbage input doesn't work
        self.assertEqual(self.project_step.embed_url, None)
        # now test a real video URL
        video_id = "6BbufUp_HNs"
        video_url = "http://www.youtube.com/watch?v=%s" % video_id
        project_step = self.create_project_step(video=video_url)
        self.assertEqual(project_step.video_id, video_id)
        self.assertEqual(project_step.embed_url, 'http://www.youtube.com/embed/%s?wmode=transparent' % video_id)

    def test_unicode_method(self):
        unicode = 'Step %d of project %s' % (self.project_step._order, self.project.title)
        self.assertEqual(self.project_step.__unicode__(), unicode)
