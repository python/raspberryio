from mezzanine.conf import settings

from raspberryio.project.tests.base import ProjectBaseTestCase
from raspberryio.search.utils import load_search_model_indexes


class SearchModelIndexeUtilsTestCase(ProjectBaseTestCase):

    def setUp(self):
        self.index_settings = {
            'auth.User': {
                'first_name': 10,
                'last_name': 5,
            }
        }
        settings.SEARCH_MODEL_INDEXES = self.index_settings

    def test_load_search_model_indexes_valid(self):
        search_proxy_model = load_search_model_indexes()[0]
        self.assertEqual(
            search_proxy_model.search_fields,
            self.index_settings['auth.User']
        )
        self.assertEqual(search_proxy_model.__name__, 'SearchableUser')
