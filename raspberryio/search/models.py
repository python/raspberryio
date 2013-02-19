from django.db import models, transaction

from mezzanine.core.managers import SearchableManager

from raspberryio.search.utils import load_search_model_indexes


class Searchable(models.Model):
    """
    An abstract base class to extend django Model classes from to make them
    searchable. Requires that the base class defines search_fields.
    """

    objects = SearchableManager()

    class Meta():
        abstract = True


class LatestArticleRevision(models.Model):
    """
    Copies the latest revision of a wiki article (wiki.ArticleRevision) when
    saved in order to create a flat list for searching.
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

searchable_models = load_search_model_indexes()
