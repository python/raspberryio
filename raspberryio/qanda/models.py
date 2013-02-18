from django.db import models
from django.db import transaction
from django.contrib.auth.models import User
from django.utils.html import strip_tags

from mezzanine.core.models import Displayable, Ownable
from mezzanine.core.fields import RichTextField
from mezzanine.utils.timezone import now


class Question(Displayable, Ownable):
    """
    A user question
    """
    question = RichTextField()

    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('question', [self.slug])


class Answer(Ownable):
    """
    An answer to a question
    """

    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers')
    answer = RichTextField()
    created_datetime = models.DateTimeField('Created')
    modified_datetime = models.DateTimeField('Modified')
    voters = models.ManyToManyField(User, related_name='answer_votes')

    class Meta:
        ordering = ['-score']

    def add_voter(self, user):
        with transaction.commit_on_success():
            if not self.voters.filter(pk=user.pk).exists():
                self.score += 1
                self.voters.add(user)
                self.save()
                return True
            return False

    def save(self, *args, **kwargs):
        # Set created and modified datetimes if not provided.
        if not self.id:
            self.created_datetime = now()
        self.modified_datetime = now()
        super(Answer, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'Answer: {0}'.format(strip_tags(self.answer))

    @models.permalink
    def get_absolute_url(self):
        return ('question', [self.question.slug])
