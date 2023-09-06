import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User

from drustvena_mrezaApp.models import *

## Defining a factory
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("first_name")


class ObjavaFactory(DjangoModelFactory):
    class Meta:
        model = Objava

    user = factory.Iterator(User.objects.all())
    sadrzaj = factory.Faker("sentence", nb_words=50)
    datum_objave = factory.Faker("date_time")
    privacy = factory.Iterator(['public', 'private', 'friends'])
    category = factory.Iterator(['tech', 'sport', 'zabava'])