from mezzanine.utils.timezone import now

from raspberryio.qanda.tests.base import QandaBaseTestCase


class QuestionTestCase(QandaBaseTestCase):

    def setUp(self):
        self.question = self.create_question()

    def test_default_score(self):
        self.assertEqual(self.question.score, 0)


class AnswerTestCase(QandaBaseTestCase):

    def setUp(self):
        self.user = self.create_user()
        self.answer_user = self.create_user()
        self.question = self.create_question(user=self.user)
        self.answer = self.create_answer(
            question=self.question, user=self.answer_user
        )

    def test_default_score(self):
        self.assertEqual(self.answer.score, 0)
