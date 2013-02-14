from django.db import models

from mezzanine.core.models import Displayable, Ownable
from mezzanine.core.fields import RichTextField

class Question(Displayable, Ownable):
    """
    A user question
    """
    question = RichTextField("Question")

    def __unicode__(self):
        return u'Question: {0}'.format(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('question', [self.slug])

class Answer(Displayable, Ownable):
    """
    An answer to a question
    """

    score = models.IntegerField()
    question = models.ForeignKey(Question)
    answer = RichTextField("Answer")

    def __unicode__(self):
        return u'Answer: {0}'.format(self.title)
