from django import forms

from raspberryio.project.forms import PlaceHolderMixin
from raspberryio.qanda.models import Question, Answer


class QuestionForm(PlaceHolderMixin, forms.ModelForm):

    class Meta(object):
        model = Question
        fields = (
            'title', 'question',
        )


class AnswerForm(PlaceHolderMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].label = 'Your Answer'

    class Meta(object):
        model = Answer
        fields = (
            'answer',
        )
