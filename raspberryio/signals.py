from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User

from actstream import action
from actstream.actions import unfollow

from wiki.models.article import Article, ArticleRevision

from raspberryio.search_models.models import LatestArticleRevision


def wiki_article_handler(sender, instance, created, **kwargs):
    revision = instance.current_revision
    if revision:
        # Copy the revision, but if it is deleted remove LatestArticleRevisions
        if not revision.deleted:
            LatestArticleRevision.copy_article_revision(revision)
        else:
            LatestArticleRevision.purge(instance)


def wiki_revision_handler(sender, instance, created, **kwargs):
    # Add wiki article edit to user's Activity Stream
    if instance.user:
        action.send(instance.user, verb='edited the wiki article', target=instance.article)
    # Create/Update LatestArticleRevision
    LatestArticleRevision.copy_article_revision(instance)


def wiki_article_delete_handler(sender, instance, **kwargs):
    # Article is purged, remove all LatestArticleRevisions if still present
    LatestArticleRevision.purge(instance)


def wiki_revision_delete_handler(sender, instance, **kwargs):
    # If a revision is somehow deleted, but the article still has a current
    # revision update LatestArtcileRevision to match that one
    if instance.article and instance.article.current_revision:
        LatestArticleRevision.copy_article_revision(
            instance.article.current_revision
        )


def user_followers_delete_handler(sender, instance, **kwargs):
    """
    Make all users unfollow the user being deleted.
    N.B. Because django-activity-stream is using a GFK, these do not cascade
    delete.
    """
    # Import act_models here. If imported at the top, this interferes with
    # appconf imports and breaks compressor configuration.
    # See https://github.com/jezdez/django_compressor/issues/333
    from actstream import models as act_models

    followers = act_models.followers(instance)
    for follower in followers:
        unfollow(follower, instance)


post_save.connect(wiki_article_handler, sender=Article)
post_save.connect(wiki_revision_handler, sender=ArticleRevision)
pre_delete.connect(wiki_article_delete_handler, sender=Article)
pre_delete.connect(wiki_article_delete_handler, sender=ArticleRevision)
pre_delete.connect(user_followers_delete_handler, sender=User)
