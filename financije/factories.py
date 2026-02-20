import factory
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import random

from .models import Account, Category, Transaction


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "test12345")


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    user = factory.SubFactory(UserFactory)
    naziv = factory.Sequence(lambda n: f"Račun {n}")
    tip = factory.Iterator(["TEKUCI", "STEDNJA", "KES"])
    pocetno_stanje = factory.LazyFunction(
        lambda: Decimal(random.randint(0, 5000))
    )


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    user = factory.SubFactory(UserFactory)
    naziv = factory.Iterator(
        ["Plaća", "Hrana", "Stan", "Prijevoz", "Zabava", "Pokloni"]
    )
    tip = factory.Iterator(["PRIHOD", "RASHOD"])


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    user = factory.SubFactory(UserFactory)
    account = factory.SubFactory(AccountFactory, user=factory.SelfAttribute("..user"))
    category = factory.SubFactory(CategoryFactory, user=factory.SelfAttribute("..user"))

    datum = factory.LazyFunction(lambda: timezone.now().date())
    iznos = factory.LazyFunction(lambda: Decimal(random.randint(5, 1500)))
    opis = factory.Faker("sentence", nb_words=3)