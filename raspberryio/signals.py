from django.db.models.signals import post_save
from actstream import action
from wiki.models.article import ArticleRevision

def wiki_actstream_handler(sender, instance, created, **kwargs):
    if instance.user:
        action.send(instance.user, verb='edited the wiki article', target=instance.article)

post_save.connect(wiki_actstream_handler, sender=ArticleRevision)
