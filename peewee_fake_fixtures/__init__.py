__author__ = "Jorge Niedbalski R. <jnr@pyrosome.org>"
import datetime
import random

import peewee
from faker import Factory

faker = Factory.create()


def fake_fixture_drop(entities):
    for name, entity in entities.items():
        entity.delete()


def fake_fixture(
    model, field_name_map={}, custom_field_type_map={}, skip_id=True, on_failure=None
):
    field_type_map = {
        peewee.DateTimeField: datetime.datetime.now,
        peewee.CharField: faker.word,
        peewee.IntegerField: random.randrange(1, 10),
        peewee.BooleanField: random.choice([True, False]),
    }

    def get_value(c, *args, **kwargs):
        if callable(c):
            return c(*args, **kwargs)
        else:
            return c

    field_type_map.update(custom_field_type_map)
    nm = model()
    for field_name, field_type in model._meta.fields.items():
        if skip_id and field_name == "id":
            continue
        else:
            if field_name in field_name_map:
                field_value = get_value(field_name_map[field_name])
            elif type(field_type) in field_type_map:
                field_value = get_value(field_type_map[type(field_type)])
            elif type(field_type) is peewee.ForeignKeyField:
                field_value = field_type.rel_model.select().first()
            elif hasattr(faker, field_name):
                field_value = getattr(faker, field_name)()
            setattr(nm, field_name, field_value)
    try:
        nm.save()
        return nm
    except Exception as ex:
        if on_failure:
            on_failure(ex.args, nm)
