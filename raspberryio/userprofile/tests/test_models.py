from raspberryio.aggregator.models import FeedType, Feed
from raspberryio.project.tests.base import RaspberryIOBaseTestCase


class ProfileTestCase(RaspberryIOBaseTestCase):

    def setUp(self):
        self.user = self.create_user()
        self.profile = self.user.get_profile()

    def test_unicode_method(self):
        self.assertEqual(self.profile.__unicode__(), self.user.username)

    def test_absolute_url(self):
        self.assertEqual(self.profile.get_absolute_url(), '/users/%s/' % self.user.username)

    def test_model_clean(self):
        "Ensure the twitter_id is stripped of the @ symbol during clean"
        self.profile.twitter_id = '@test'
        self.profile.clean()
        self.profile.save()
        self.assertFalse('@' in self.profile.twitter_id)

    def test_feed_owner(self):
        "Determine if the user owns and Aggregator.Feed instances"
        self.assertFalse(self.profile.feed_owner)

        self.feed_type = FeedType(name="Test Feed Type", slug="test-feed-type", can_self_add=True)
        self.feed_type.save()
        self.approved_feed = Feed(title="Approved", feed_url="foo.com/rss/", public_url="foo.com/", is_defunct=False,
                             feed_type=self.feed_type, owner=self.profile.user)
        self.approved_feed.save()
        self.assertTrue(self.profile.feed_owner)
