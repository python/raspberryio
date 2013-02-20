"""
Models here provide search capability for those that can't be queried directly
by Mezzanine's SearchableManager. For example, the wiki.ArticleRevision model
tracks every revision to a wiki page. Searching on it directly would return
every revision rather than the latest. (i.e. a flat structure is needed)
"""
from django.db import models, transaction


class LatestArticleRevision(models.Model):
    """
    Copies the latest revision of a wiki article (wiki.ArticleRevision) when
    saved or deleted in order to create a flat list for searching.
    """

    article_id = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=512, null=False, blank=False)
    content = models.TextField(blank=True)

    search_classname = 'Wiki Article'

    @classmethod
    def copy_article_revision(kls, revision):
        """
        Create/Update LatestArticleRevision from an ArticleRevision instance
        """
        with transaction.commit_on_success():
            latest_article, lar_created = kls.objects.get_or_create(
                article_id=revision.article.id,
            )
            latest_article.title = revision.title
            latest_article.content = revision.content
            latest_article.save()

    @classmethod
    def purge(kls, article):
        """
        Remove LatestArticleRevision whose article was deleted or purged
        """
        kls.objects.filter(article_id=article.id).delete()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('wiki:get', (self.article_id,))
