peewee_fake_fixtures
====================

Fake fixtures generator for peewee

Usage
=====

* Install from pip 
```shell
    pip install peewee-fake-fixtures
```

Just load your model classes and call ``fake_fixture`` method to load 
randomly auto-generate fixtures on the database

```python

from model import User, Reservation, PhoneNumber, APIKey
 
added_objects = fake_fixture({
    APIKey: {},
    User: {
        'active': True #you can override default values
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
