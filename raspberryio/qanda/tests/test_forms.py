from django.test.client import RequestFactory
from django.contrib.sites.models import Site

from mezzanine.utils.sites import current_site_id
from actstream.models import Action

from raspberryio.qanda.tests.base import QandaBaseTestCase
from raspberryio.qanda.models import Question, Answer
from raspberryio.qanda.forms import QuestionForm, AnswerForm


class QuestionFormTestCase(QandaBaseTestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.question = self.create_question()

    def test_edit_invalid(self):
        request = self.request_factory.post('/', {})
        form = QuestionForm(request.POST, instance=self.question)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], ['This field is required.'])
        self.assertEqual(form.errors['question'], ['This field is required.'])
        self.assertEqual(Action.objects.count(), 0,
            'Invalid form submission should not result in an action'
        )

    def test_create_invalid(self):
        request = self.request_factory.post('/', {})
        site = Site.objects.get(id=current_site_id)
        question = Question(user=self.create_user(), site=site)
        form = QuestionForm(request.POST, instance=question)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], ['This field is required.'])
        self.assertEqual(form.errors['question'], ['This field is required.'])
        self.assertEqual(Action.objects.count(), 0,
            'Invalid form submission should not result in an action'
        )

    def test_edit_valid(self):
        post_data = {
            'title': self.get_random_string(),
            'question': self.get_random_string(),
        }
        request = self.request_factory.post('/', post_data)
        form = QuestionForm(request.POST, instance=self.question)
        if form.is_valid():
            form.save()
            self.assertEqual(Action.objects.count(), 0,
                'editting a question should not result in an action'
            )
        else:
            self.fail('Form should be valid')

    def test_create_valid(self):
        post_data = {
            'title': self.get_random_string(),
            'question': self.get_random_string(),
        }
        request = self.request_factory.post('/', post_data)
        site = Site.objects.get(id=current_site_id)
        question = Question(user=self.create_user(), site=site)
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            self.assertEqual(Action.objects.count(), 1,
                'Creating a question should result in an action'
            )
        else:
            self.fail('Form should be valid')

class AnswerFormTestCase(QandaBaseTestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.question = self.create_question()
        self.answer = self.create_answer(question=self.question)

    def test_edit_invalid(self):
        request = self.request_factory.post('/', {})
        form = AnswerForm(request.POST, instance=self.answer)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['answer'], ['This field is required.'])
        self.assertEqual(Action.objects.count(), 0,
            'Invalid form submission should not result in an action'
        )

    def test_create_invalid(self):
        request = self.request_factory.post('/', {})
        answer = Answer(user=self.create_user(), question=self.question)
        form = AnswerForm(request.POST, instance=answer)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['answer'], ['This field is required.'])
        self.assertEqual(Action.objects.count(), 0,
            'Invalid form submission should not result in an action'
        )

    def test_edit_valid(self):
        post_data = {
            'answer': self.get_random_string(),
        }
        request = self.request_factory.post('/', post_data)
        form = AnswerForm(request.POST, instance=self.answer)
        if form.is_valid():
            form.save()
            self.assertEqual(Action.objects.count(), 0,
                'editting an answer should not result in an action'
            )
        else:
            self.fail('Form should be valid')

    def test_create_valid(self):
        post_data = {
            'answer': self.get_random_string(),
        }
        request = self.request_factory.post('/', post_data)
        answer = Answer(user=self.create_user(), question=self.question)
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            self.assertEqual(Action.objects.count(), 1,
                'Creating an answer should result in an action'
            )
        else:
            self.fail('Form should be valid')
