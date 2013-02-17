from raspberryio.project.tests.base import RaspberryIOBaseTestCase
from raspberryio.qanda.models import Question, Answer


class QandaBaseTestCase(RaspberryIOBaseTestCase):
    """
    Base TestCase class that provides utilities for the qanda app
    """

    def create_question(self, **kwargs):
        defaults = {
            'title': self.get_random_string(length=500),
            'site': kwargs.pop('site', self.create_site()),
            'user': kwargs.pop('user', self.create_user()),
            'question': self.get_random_string(length=100),
        }
        return self.create_instance(Question, defaults=defaults, **kwargs)

    def create_answer(self, **kwargs):
        defaults = {
            'user': kwargs.pop('user', self.create_user()),
            'question': kwargs.pop('question', self.create_question()),
            'answer': self.get_random_string(length=100),
        }
        return self.create_instance(Answer, defaults=defaults, **kwargs)
