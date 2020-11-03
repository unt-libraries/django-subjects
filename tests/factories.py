import factory.fuzzy
from subjects import models


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Subject

    name = factory.fuzzy.FuzzyText()
    parent = factory.fuzzy.FuzzyInteger(0)
    lft = factory.fuzzy.FuzzyInteger(0)
    rght = factory.fuzzy.FuzzyInteger(0)
    keywords = factory.fuzzy.FuzzyText()
    notes = factory.fuzzy.FuzzyText()
