#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jorge Niedbalski R. <jnr@pyrosome.org>'

import peewee
import random
import datetime
import logging
import json

from peewee import sort_models_topologically
from faker import Factory

logger = logging.getLogger()
faker = Factory.create()


def fake_fixture_drop(entities):
    for name, entity in entities.items():
        entity.delete()
        logger.info('Removed %s->id = %d' % (name, entity.id))


def fake_fixture(models, field_type_map=None, skip_id=True,
                        on_failure=None):

    default_field_type_map = {
        peewee.DateTimeField: datetime.datetime.now,
        peewee.CharField: faker.word,
        peewee.IntegerField: random.randrange(1, 10)
    }

    def get_value(c, *args, **kwargs):
        if callable(c):
            return c(*args, **kwargs)
        else:
            return c

    sorted_models = sort_models_topologically(models.keys())
    added_objects = {}

    if field_type_map is None:
        field_type_map = default_field_type_map

    for model in sorted_models:
        nm = model()
        logger.info('Creating new:%s model' % model._meta.name)
        for field in model._meta.get_fields():
            if skip_id and field.name in ('id',):
                continue
            else:
                if hasattr(faker, field.name):
                    field_value = getattr(faker, field.name)()
                elif field.name in models[model]:
                    field_value = get_value(models[model][field.name])
                elif type(field) in field_type_map:
                    field_value = get_value(field_type_map[type(field)])
                else:
                    if type(field) is peewee.ForeignKeyField:
                        if field.rel_model._meta.name in added_objects:
                            field_value = field.rel_model.get(id=
                                        added_objects[field.rel_model._meta.name].id)

                logger.info('Setting: %s.%s==%s' % (model._meta.name,
                                                    field.name, field_value))
                setattr(nm, field.name, field_value)
        try:
            nm.save()
        except Exception as ex:
            logger.warn(ex.message)
            if on_failure:
                on_failure(ex.message, nm, added_objects)
        else:
            logger.info('Added model: %s->id = %d' % (nm._meta.name, nm.id))
            added_objects[nm._meta.name] = nm

    return added_objects
