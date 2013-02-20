from mezzanine.conf import settings

from raspberryio.project.tests.base import ProjectBaseTestCase
from raspberryio.search.utils import load_search_model_indexes


class SearchModelIndexeUtilsTestCase(ProjectBaseTestCase):

    def setUp(self):
        """
        FIXME: This test depends on the current settings, which has auth.user
        in the SEARCH_MODEL_INDEXES setting.
        """
        self.index_settings = settings.SEARCH_MODEL_INDEXES

    def test_load_search_model_indexes_valid(self):
        search_proxy_model = load_search_model_indexes()[1]
        self.assertEqual(
            search_proxy_model.search_fields,
            self.index_settings['auth.user']
        )
        self.assertEqual(search_proxy_model.__name__, 'SearchableUser')
