peewee_fake_fixtures
====================

Fake fixtures generator for peewee, it populates the models with
random data depending on the field type.

Useful for auto-generate fixtures and other testing tools.

Usage
=====

* Install from pip 
```
    pip install peewee-fake-fixtures
```

Just load your model classes and call ``fake_fixture`` method to load 
randomly auto-generate fixtures on the database

```python

from model import User, Pet
 
added_objects = fake_fixture({
    User,
    field_name_map={
    'name': 'fjl', "password": '123456'
    },  #you can override default values
    custom_field_type_map={
        IntegerField: 100  # override default field,
    },
    Reservation: {
        'status': ('PENDING', 'pending')
    },
    PhoneNumber: {
        'status': ('CONFIRMED', 'confirmed'),
        'value': faker.phoneNumber
    }},
    skip_id=True, #don't generate ID fields
    on_failure=lambda x,y,z: fake_fixture_drop(z) #On failure callback
)
 
 
fake_fixture_drop(added_objects) #Remove fixtures from database

```
