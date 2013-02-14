from django import forms
from raspberryio.project.forms import PlaceHolderMixin
from raspberryio.qanda.models import Question

class QuestionForm(PlaceHolderMixin, forms.ModelForm):

    class Meta(object):
        model = Question
        fields = (
            'title', 'question',
        )
