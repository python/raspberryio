from raspberryio.project.tests.base import RaspberryIOBaseTestCase


class ProfileTestCase(RaspberryIOBaseTestCase):

    def setUp(self):
        self.user = self.create_user()
        self.profile = self.user.get_profile()

    def test_model_clean(self):
        "Ensure the twitter_id is stripped of the @ symbol during clean"
        self.profile.twitter_id = '@test'
        self.profile.clean()
        self.profile.save()
        self.assertFalse('@' in self.profile.twitter_id)
