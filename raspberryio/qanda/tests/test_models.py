from raspberryio.qanda.tests.base import QandaBaseTestCase


class AnswerTestCase(QandaBaseTestCase):

    def setUp(self):
        self.user = self.create_user()
        self.answer_user = self.create_user()
        self.question = self.create_question(user=self.user)
        self.answer = self.create_answer(
            question=self.question, user=self.answer_user
        )

    def test_unicode_method(self):
        title = 'My title'
        q = self.create_question(title=title)
        a = self.create_answer(question=q)
        self.assertEqual(q.__unicode__(), title)
        self.assertEqual(a.__unicode__(), title)

    def test_default_score(self):
        self.assertEqual(self.answer.score, 0)

    def test_add_voter_new(self):
        self.answer.score = 10
        self.answer.save()
        result = self.answer.add_voter(self.user)
        self.assertEqual(self.answer.score, 11)
        self.assertEqual(list(self.answer.voters.all()), [self.user],
            'answer.voters should contain the user once and only once'
        )
        self.assertTrue(result)

    def test_add_voter_existing(self):
        result = self.answer.add_voter(self.user)
        self.assertEqual(self.answer.score, 1)
        self.assertTrue(result)
        result = self.answer.add_voter(self.user)
        self.assertFalse(result)
        self.assertEqual(self.answer.score, 1)
        self.assertEqual(list(self.answer.voters.all()), [self.user],
            'answer.voters should contain the user once and only once'
        )

    def test_add_multiple_voters(self):
        result = self.answer.add_voter(self.user)
        self.assertEqual(self.answer.score, 1)
        self.assertTrue(result)
        other_user = self.create_user()
        users = (self.user, other_user)
        result = self.answer.add_voter(other_user)
        self.assertEqual(self.answer.score, 2)
        self.assertTrue(result)
        self.assertEqual(set(self.answer.voters.all()), set(users),
            'answer.voters should contain both users'
        )
