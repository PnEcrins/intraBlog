from factory.django import DjangoModelFactory
from django.contrib.auth.models import Group

class GroupFactory(DjangoModelFactory):
    name = "test"
    class Meta:
        model = Group