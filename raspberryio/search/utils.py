"""
Utilities for cleaning the SEARCH_MODEL_INDEXES definition and generating the
search proxy models
"""

import logging

from django.db import models

from mezzanine.conf import settings


def load_search_model_indexes():
    """
    Create proxy models that subclass Searchable and have search_fields as
    defined by SEARCH_MODEL_INDEXES.

    Sets the SEARCH_MODEL_CHOICES setting from the SEARCH_MODEL_INDEXES keys as
    a side-effect.
    """
    index = settings.SEARCH_MODEL_INDEXES
    model_fields = clean_index(index.items())
    model_fields = clean_model_fields(model_fields)
    settings.SEARCH_MODEL_CHOICES = index.keys()
    return [
        make_search_proxy_model(ModelKls, search_fields)
        for ModelKls, search_fields in model_fields
    ]


def clean_model_fields(model_fields):
    """
    Given a list of models and search_field dictionaries, returns the provided
    list with any fields removed that were not found on their respective models

    Expected input is a list of two tuples in the form of:
        [(ModelClass, search_fields_dictionary), ...]
    """
    for ModelKls, fields in model_fields:
        model_field_names = [field.name for field in ModelKls._meta.fields]
        field_keys = fields.keys()
        for field_key in field_keys:
            if field_key not in model_field_names:
                fields.pop(field_key)
                err_msg = 'SEARCH_MODEL_INDEXES has a field {0} for the ' + \
                'model {1} that does not exist'.format(field_key, ModelKls)
                logging.error(err_msg)
    return model_fields


def clean_index(index):
    """
    Given a list of model paths and search_field dictionaries, returns a list
    of imported model classes and search_field dictionaries for all models that
    could be imported.

    Expected input:
        [('appname.model', search_fields_dictionary), ...]
    """

    model_classes_fields = []
    for appname_model, fields in index:
        try:
            appname, modelname = appname_model.split('.')
        except (TypeError, ValueError):
            err_msg = 'SEARCH_MODEL_INDEXES setting key {0} is in the' + \
            'wrong format'.format(appname_model)
            logging.error(err_msg)
            continue
        ModelKls = models.get_model(appname, modelname)
        if ModelKls is None:
            err_msg = 'SEARCH_MODEL_INDEXES key {0} refers to a model' + \
            'that cannot be found.'.format(appname_model)
            logging.error(err_msg)
            continue
        model_classes_fields.append((ModelKls, fields))
    return model_classes_fields


def make_search_proxy_model(ModelKls, search_fields):
    """
    Given a Django model class, and a dictionary of search fields, create and
    return a proxy model that subclasses Searchable and has search_fields equal
    to the search_fields provided.
    """

    kls_name = 'Searchable' + ModelKls.__name__

    class Meta(object):
        proxy = True

    # get_models fails to load abstract models. Import is here to avoid
    # ciruclar imports
    from raspberryio.search.models import Searchable

    return type(kls_name, (Searchable, ModelKls), {
        'search_fields': search_fields,
        'search_classname': ModelKls.__name__.lower(),
        'Meta': Meta,
        '__module__': ModelKls.__module__
    })
