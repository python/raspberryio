from django.db import models

from mezzanine.core.models import Displayable, Ownable
from mezzanine.core.fields import RichTextField


class Question(Displayable, Ownable):
    """
    A user question
    """
    question = RichTextField()
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return u'Question: {0}'.format(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('question', [self.slug])


class Answer(Displayable, Ownable):
    """
    An answer to a question
    """

    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers')
    answer = RichTextField()

    def __unicode__(self):
        return u'Answer: {0}'.format(self.title)
