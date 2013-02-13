from django.db import models

from mezzanine.core.managers import SearchableManager


class Searchable(models.Model):
    """
    An abstract base class to extend django Model classes from to make them
    searchable. Requires the base class to define search_fields
    """

    objects = SearchableManager()

    class Meta(object):
        abstract = True
