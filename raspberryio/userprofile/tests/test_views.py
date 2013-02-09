from django.core.urlresolvers import reverse

from raspberryio.project.tests.base import RaspberryIOBaseTestCase

from actstream.actions import follow


class RelationshipTestCase(RaspberryIOBaseTestCase):
    url_name = 'profile-related'

    def setUp(self):
        self.user = self.create_user(data={'username': 'test'})
        self.user1 = self.create_user(data={'username': 'test1'})

    def get_url_args(self, user, relationship):
        return reverse(self.url_name, args=(user, relationship))

    def test_no_followers(self):
        url = self.get_url_args(self.user, 'followers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        related_users = len(response.context['related_users'])
        self.assertEqual(related_users, self.user.follow_set.all().count())

    def test_not_following(self):
        url = self.get_url_args(self.user, 'following')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        related_users = len(response.context['related_users'])
        self.assertEqual(related_users, self.user.follow_set.all().count())

    def test_followers(self):
        follow(self.user1, self.user)
        url = self.get_url_args(self.user, 'followers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        related_users = len(response.context['related_users'])
        self.assertEqual(related_users, self.user1.follow_set.all().count())

    def test_following(self):
        follow(self.user, self.user1)
        url = self.get_url_args(self.user, 'following')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        related_users = len(response.context['related_users'])
        self.assertEqual(related_users, self.user.follow_set.all().count())
