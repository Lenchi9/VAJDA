from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import random

from financije.factories import (
    AccountFactory,
    CategoryFactory,
    TransactionFactory,
)
from financije.models import Account, Category, Transaction


class Command(BaseCommand):
    help = "Puni bazu testnim podacima"

    def add_arguments(self, parser):
        parser.add_argument("--accounts", type=int, default=2)
        parser.add_argument("--categories", type=int, default=6)
        parser.add_argument("--transactions", type=int, default=30)
        parser.add_argument("--username", type=str, default="admin")

    def handle(self, *args, **options):
        username = options["username"]

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password("admin12345")
            user.is_staff = True
            user.is_superuser = True
            user.save()

        for _ in range(options["accounts"]):
            AccountFactory(user=user)

        for _ in range(options["categories"]):
            CategoryFactory(user=user)

        user_accounts = list(Account.objects.filter(user=user))
        user_categories = list(Category.objects.filter(user=user))

        for _ in range(options["transactions"]):
            TransactionFactory(
                user=user,
                account=random.choice(user_accounts),
                category=random.choice(user_categories),
            )

        self.stdout.write(self.style.SUCCESS(
            f"Baza napunjena! "
            f"Accounts={Account.objects.filter(user=user).count()} | "
            f"Categories={Category.objects.filter(user=user).count()} | "
            f"Transactions={Transaction.objects.filter(user=user).count()}"
        ))