from urllib import urlencode

from hilbert.test import ViewTestMixin
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED

from raspberryio.project.tests.base import ProjectBaseTestCase


class SearchViewTestCase(ViewTestMixin, ProjectBaseTestCase):
    """
    FIXME: This test is dependent on settings.SEARCH_MODEL_INDEXES. Need to
    find a way to unit test the search functionality independent of settings
    """

    url_name = 'search'

    def setUp(self):
        super(SearchViewTestCase, self).setUp()
        self.user = self.create_user(data={'password': 'password'})
        self.project = self.create_project(title='project1', user=self.user,
            status=CONTENT_STATUS_PUBLISHED
        )

    def get_query_params(self, query='', object_type=None):
        object_type = object_type or {}
        query_dict = {
            'q': query,
        }
        query_dict.update({
            'type': object_type
        })
        return '?' + urlencode(query_dict)

    def test_empty_result(self):
        self.project.delete()
        self.user.delete()
        response = self.client.get(self.url + self.get_query_params(''))
        results = response.context['results'].object_list
        self.assertEqual(results, [])

    def test_one_result(self):
        # Create a project that should not appear in the results
        self.create_project(
            title='zzz', user=self.user, status=CONTENT_STATUS_PUBLISHED
        )
        query = self.get_query_params(self.project.title)
        response = self.client.get(self.url + query)
        results = response.context['results'].object_list
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, self.project.title)

    def test_many_results_one_type(self):
        project2 = self.create_project(
            title='project2', user=self.user, status=CONTENT_STATUS_PUBLISHED
        )
        query = self.get_query_params('project')
        response = self.client.get(self.url + query)
        results = response.context['results'].object_list
        result_titles = [result.title for result in results]
        self.assertEqual(len(results), 2)
        self.assertEqual(
            set(result_titles), set([self.project.title, project2.title])
        )

    def test_many_results_many_types(self):
        project2 = self.create_project(
            title='project2', user=self.user, status=CONTENT_STATUS_PUBLISHED
        )
        user2 = self.create_user(data={'username': 'PRoJect'})
        query = self.get_query_params('project')
        response = self.client.get(self.url + query)
        results = response.context['results'].object_list
        result_urls = [result.get_absolute_url() for result in results]
        expected_results = set(map(lambda i: i.get_absolute_url(), [
            self.project, project2, user2,
        ]))
        self.assertEqual(len(results), 3)
        self.assertEqual(set(result_urls), expected_results)

    def test_query_type_malformed(self):
        project2 = self.create_project(
            title='project2', user=self.user, status=CONTENT_STATUS_PUBLISHED
        )
        user2 = self.create_user(data={'username': 'PRoJect'})
        query = self.get_query_params('project', 'asdfasdfasdf')
        response = self.client.get(self.url + query)
        results = response.context['results'].object_list
        result_urls = [result.get_absolute_url() for result in results]
        expected_results = set(map(lambda i: i.get_absolute_url(), [
            self.project, project2, user2
        ]))
        # Everything returns because the given 'type' is invalid
        self.assertEqual(len(results), 3)
        self.assertEqual(set(result_urls), expected_results)

    def test_query_unregistered_model(self):
        project2 = self.create_project(
            title='project2', user=self.user, status=CONTENT_STATUS_PUBLISHED
        )
        user2 = self.create_user(data={'username': 'PRoJect'})
        query = self.get_query_params('project', 'project.projectimage')
        response = self.client.get(self.url + query)
        results = response.context['results'].object_list
        result_urls = [result.get_absolute_url() for result in results]
        expected_results = set(map(lambda i: i.get_absolute_url(), [
            self.project, project2, user2
        ]))
        # Everything returns because the given 'type' is invalid
        self.assertEqual(len(results), 3)
        self.assertEqual(set(result_urls), expected_results)

    def test_query_on_type(self):
        project2 = self.create_project(
            title='project2', user=self.user, status=CONTENT_STATUS_PUBLISHED
        )
        # Created user should not return because query is for project type
        self.create_user(data={'username': 'PRoJect'})
        query = self.get_query_params('project', 'project.project')
        response = self.client.get(self.url + query)
        results = response.context['results'].object_list
        result_urls = [result.get_absolute_url() for result in results]
        expected_results = set(map(lambda i: i.get_absolute_url(), [
            self.project, project2
        ]))
        self.assertEqual(len(results), 2)
        self.assertEqual(set(result_urls), expected_results)

    def test_draft_removed(self):
        # Create a project in the draft status (unpublished)
        self.create_project(title='project2', user=self.user)
        query = self.get_query_params('project')
        response = self.client.get(self.url + query)
        results = response.context['results'].object_list
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, self.project.title)
