from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from raspberryio.project.tests.base import ProjectBaseTestCase, RaspberryIOBaseTestCase

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


class DashboardTestCase(ProjectBaseTestCase):
    url_name = 'profile-dashboard'

    def setUp(self):
        self.user = self.create_user(data={'username': 'test', 'password': 'pwd'})
        self.user1 = self.create_user(data={'username': 'test1', 'password': 'pwd'})
        self.user2 = self.create_user(data={'username': 'test2', 'password': 'pwd'})
        self.project1 = self.create_project(user=self.user1)
        self.url = reverse(self.url_name)

    def test_not_following(self):
        self.client.login(username=self.user.username, password='pwd')
        response = self.client.get(self.url)
        actions = len(response.context['actions'])
        self.assertEqual(actions, self.user.follow_set.all().count())

    def test_following(self):
        follow(self.user, self.user1)
        follow(self.user, self.user2)
        # have 1 & 2 follow each other to generate actions
        follow(self.user1, self.user2)
        follow(self.user2, self.user1)
        self.client.login(username=self.user.username, password='pwd')
        response = self.client.get(self.url)
        actions = len(response.context['actions'])
        self.assertEqual(actions, 2)

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class ActiveUsersTestCase(RaspberryIOBaseTestCase):
    url_name = 'profile-users'

    def setUp(self):
        self.user = self.create_user(data={'username': 'test', 'password': 'pwd'})
        self.user1 = self.create_user(data={'username': 'test1', 'password': 'pwd'})
        self.user2 = self.create_user(data={'username': 'test2', 'password': 'pwd'})
        self.url = reverse(self.url_name)

    def test_active_users(self):
        response = self.client.get(self.url)
        users = response.context['users']
        self.assertEqual(len(users), User.objects.all().count())

    def test_inactive_users(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.get(self.url)
        users = response.context['users']
        self.assertEqual(len(users), User.objects.filter(is_active=True).count())
