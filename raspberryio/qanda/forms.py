from django import forms

from actstream import action


from raspberryio.project.forms import PlaceHolderMixin
from raspberryio.qanda.models import Question, Answer


class QuestionForm(PlaceHolderMixin, forms.ModelForm):

    def save(self, *args, **kwargs):
        created = self.instance.id is None
        question = super(QuestionForm, self).save(*args, **kwargs)
        if created:
            action.send(question.user, verb='asked', target=question)
        return question

    class Meta(object):
        model = Question
        fields = (
            'title', 'question',
        )


class AnswerForm(PlaceHolderMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].label = 'Your Answer'

    def save(self, *args, **kwargs):
        created = self.instance.id is None
        answer = super(AnswerForm, self).save(*args, **kwargs)
        if created:
            action.send(answer.user, verb='answered', target=answer)
        return answer

    class Meta(object):
        model = Answer
        fields = (
            'answer',
        )
