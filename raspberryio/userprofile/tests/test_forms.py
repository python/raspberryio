from django.core.urlresolvers import reverse

from raspberryio.project.tests.base import RaspberryIOBaseTestCase


class UserProfileFormTestCase(RaspberryIOBaseTestCase):
    url_name = "profile_update"

    def setUp(self):
        self.user = self.create_user(data={'username': 'test', 'password': 'pwd'})
        self.url = reverse(self.url_name)

    def test_twitter_handle_on_form(self):
        self.client.login(username=self.user.username, password='pwd')
        response = self.client.get(self.url)
        twitter_el = '<input type="text" placeholder="Twitter Id" name="twitter_id" id="id_twitter_id" />'
        self.assertContains(response, twitter_el, html=True)
