import pendulum
from peewee import *

from peewee_fake_fixtures import fake_fixture

db = SqliteDatabase("test.db")


class User(Model):
    class Meta:
        database = db

    name = CharField()
    password = CharField()
    age = IntegerField()
    register_time = DateTimeField(default=pendulum.now())


class Pet(Model):
    class Meta:
        database = db

    name = CharField()
    owner = ForeignKeyField(User, field=User.name, column_name="owner_name")
    birthday = DateTimeField()


def test_fake_fixture():
    db.connect()
    db.create_tables([User, Pet])
    fake_fixture(User)
    pet = fake_fixture(Pet)
    assert pet.owner_name == pet.owner.name
    field_name_map = {'name': 'fjl', "password": '123456'}
    fjl = fake_fixture(User, field_name_map={'name': 'fjl', "password": '123456'})
    assert fjl.password == field_name_map['password']
    assert fjl.name == field_name_map['name']
    foo = fake_fixture(User, custom_field_type_map={IntegerField: 100})
    assert foo.age == 100


test_fake_fixture()
