from django.core.urlresolvers import reverse

from hilbert.test import ViewTestMixin, AuthViewMixin

from raspberryio.qanda.tests.base import QandaBaseTestCase
from raspberryio.qanda.models import Question, Answer


class QuestionListViewTestCase(ViewTestMixin, QandaBaseTestCase):
    url_name = 'question-list'

    def setUp(self):
        self.user = self.create_user(data={'password': 'password'})
        super(QuestionListViewTestCase, self).setUp()

    def test_results(self):
        question1 = self.create_question()
        question2 = self.create_question()
        question3 = self.create_question()
        expected_questions = set([question1, question2, question3])
        response = self.client.get(self.url)
        result_questions = response.context['questions']
        self.assertEqual(set(result_questions), expected_questions)


class QuestionDetailViewTestCase(ViewTestMixin, QandaBaseTestCase):
    url_name = 'question'

    def setUp(self):
        self.user = self.create_user(data={'password': 'password'})
        self.question = self.create_question(user=self.user)
        super(QuestionDetailViewTestCase, self).setUp()

    def get_url_args(self):
        return (self.question.slug,)

    def test_answers(self):
        answer1 = self.create_answer(question=self.question)
        answer2 = self.create_answer(question=self.question)
        expected_answers = set([answer1, answer2])
        response = self.client.get(self.url)
        result_answers = response.context['answers']
        self.assertEqual(set(result_answers), expected_answers)

    def test_votes(self):
        self.client.login(username=self.user.username, password='password')
        answer = self.create_answer(question=self.question)
        self.create_answer(question=self.question)
        other_answer = self.create_answer()
        answer.add_voter(self.user)
        other_answer.add_voter(self.user)
        response = self.client.get(self.url)
        user_votes = response.context['votes']
        self.assertEqual(set(user_votes), set([answer.pk]),
            "Only the current question's answers the user voted on should appear in 'votes'"
        )


class QuestionCreateEditViewTestCase(AuthViewMixin, QandaBaseTestCase):
    url_name = 'question-create-edit'

    def setUp(self):
        super(QuestionCreateEditViewTestCase, self).setUp()
        self.question = self.create_question(user=self.user)

    def get_edit_url(self, question_slug=''):
        """
        self.url points to using the view for creating a new question. Use
        this helper to create a link to the edit view.
        """
        return reverse(
            self.url_name, args=(question_slug or self.question.slug,)
        )

    def test_bad_slug(self):
        url = self.get_edit_url('bad-slug')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_valid(self):
        data = {
            'title': 'question title',
            'question': 'I want to know about things',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        question = Question.objects.get(title=data['title'])
        self.assertEqual(question.user, self.user)
        self.assertEqual(question.question, data['question'])

    def test_create_invalid(self):
        data = {
            'title': '',
            'question': 'I want to know about things',
        }
        response = self.client.post(self.url, data)
        question_form = response.context['question_form']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            question_form.errors, {'title': [u'This field is required.']}
        )

    def test_edit_valid(self):
        data = {
            'title': 'updated title',
            'question': 'edit: I want to know about some more things',
        }
        response = self.client.post(self.get_edit_url(), data)
        self.assertEqual(response.status_code, 302)
        question = Question.objects.get(title=data['title'])
        self.assertEqual(question.title, data['title'])
        self.assertEqual(question.question, data['question'])

    def test_edit_invalid(self):
        data = {
            'title': 'updated title',
            'question': '',
        }
        response = self.client.post(self.get_edit_url(), data)
        question_form = response.context['question_form']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            question_form.errors, {'question': [u'This field is required.']}
        )

    def test_edit_superuser(self):
        data = {
            'title': 'updated title by superuser',
            'question': 'edit: I am a superuser and I want to change this',
        }
        response = self.client.post(self.get_edit_url(), data)
        self.assertEqual(response.status_code, 302)
        question = Question.objects.get(title=data['title'])
        self.assertEqual(question.title, data['title'])
        self.assertEqual(question.question, data['question'])

    def test_edit_other_user_forbidden(self):
        other_user = self.create_user(data={'password': 'password'})
        data = {
            'title': 'updated title by other user',
            'question': 'edit: I am the wrong person to edit this',
        }
        self.client.logout()
        self.client.login(username=other_user.username, password='password')
        response = self.client.post(self.get_edit_url(), data)
        self.assertEqual(response.status_code, 403)
        question = Question.objects.get(pk=self.question.pk)
        self.assertEqual(question.title, self.question.title)
        self.assertEqual(question.question, self.question.question)


class AnswerCreateEditViewTestCase(QandaBaseTestCase):
    url_name = 'answer-create-edit'

    def setUp(self):
        self.user = self.create_user(data={'password': 'password'})
        self.question = self.create_question()
        self.answer = self.create_answer(
            user=self.user, question=self.question
        )
        self.client.login(username=self.user.username, password='password')
        self.url = reverse(self.url_name, args=self.get_url_args())

    def get_url_args(self):
        return (self.question.slug,)

    def get_edit_url(self, question_slug='', answer_pk=None):
        """
        self.url points to using the view for creating a new question. Use
        this helper to create a link to the edit view.
        """
        url_args = (
            question_slug or self.question.slug,
            answer_pk or self.answer.pk,
        )
        return reverse(self.url_name, args=url_args)

    def test_bad_question_slug(self):
        url = self.get_edit_url('bad-slug')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_bad_answer_pk(self):
        url = self.get_edit_url(answer_pk=9999)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_valid(self):
        data = {
            'answer': 'The answer is rm -rf'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        answer = Answer.objects.get(answer=data['answer'])
        self.assertEqual(answer.user, self.user)

    def test_create_invalid(self):
        data = {
            'answer': '',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        answers = Answer.objects.all()
        self.assertEqual(list(answers), [self.answer])

    def test_edit_valid(self):
        data = {
            'answer': 'Edit: On second thought, you probably should not rm -rf'
        }
        response = self.client.post(self.get_edit_url(), data)
        self.assertEqual(response.status_code, 302)
        answer = Answer.objects.get(pk=self.answer.pk)
        self.assertEqual(answer.user, self.user)
        self.assertEqual(answer.answer, data['answer'])

    def test_edit_invalid(self):
        data = {
            'answer': '',
        }
        response = self.client.post(self.get_edit_url(), data)
        self.assertEqual(response.status_code, 302)
        answer = Answer.objects.get(pk=self.answer.pk)
        self.assertEqual(answer.user, self.user)
        self.assertEqual(answer.answer, self.answer.answer)


class UpvoteAnswerViewTestCase(QandaBaseTestCase):
    url_name = 'upvote-answer'

    def setUp(self):
        self.user = self.create_user(data={'password': 'password'})
        self.question = self.create_question()
        self.answer = self.create_answer(question=self.question)
        self.client.login(username=self.user.username, password='password')
        self.url = reverse(self.url_name, args=self.get_url_args())

    def get_url_args(self):
        return (self.answer.pk,)

    def test_bad_pk(self):
        url = reverse(self.url_name, args=(9999,))
        response = self.client.get(url, is_ajax=True)
        self.assertEqual(response.status_code, 404)
        answer = Answer.objects.get(pk=self.answer.pk)
        self.assertEqual(answer.score, 0)
        self.assertEqual(answer.voters.count(), 0)

    def test_not_ajax(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        answer = Answer.objects.get(pk=self.answer.pk)
        self.assertEqual(answer.score, 0)
        self.assertEqual(answer.voters.count(), 0)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url, is_ajax=True)
        self.assertEqual(response.status_code, 302)
        answer = Answer.objects.get(pk=self.answer.pk)
        self.assertEqual(answer.score, 0)
        self.assertEqual(answer.voters.count(), 0)

    def test_new_vote(self):
        response = self.client.get(self.url, is_ajax=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'true')
        answer = Answer.objects.get(pk=self.answer.pk)
        self.assertEqual(list(answer.voters.all()), [self.user])
        self.assertEqual(answer.score, 1)

    def test_existing_vote(self):
        self.answer.add_voter(self.user)
        response = self.client.get(self.url, is_ajax=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'false')
        answer = Answer.objects.get(pk=self.answer.pk)
        self.assertEqual(list(answer.voters.all()), [self.user])
        self.assertEqual(answer.score, 1)
