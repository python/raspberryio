
from django.db import models

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

load_search_model_indexes()
