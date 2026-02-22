from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from financije.models import Transaction
from financije.factories import UserFactory, AccountFactory, CategoryFactory, TransactionFactory


class AuthAccessTests(TestCase):
    def test_transaction_list_requires_login(self):
        url = reverse("transaction_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_account_list_requires_login(self):
        url = reverse("account_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_category_list_requires_login(self):
        url = reverse("category_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])


class UserIsolationTests(TestCase):
    def setUp(self):
        self.user1 = UserFactory(username="korisnik1")
        self.user2 = UserFactory(username="korisnik2")

        self.acc1 = AccountFactory(user=self.user1, naziv="Racun 1")
        self.cat1 = CategoryFactory(user=self.user1, naziv="Kategorija 1")
        self.t1 = TransactionFactory(user=self.user1, account=self.acc1, category=self.cat1, opis="Transakcija U1")

        self.acc2 = AccountFactory(user=self.user2, naziv="Racun 2")
        self.cat2 = CategoryFactory(user=self.user2, naziv="Kategorija 2")
        self.t2 = TransactionFactory(user=self.user2, account=self.acc2, category=self.cat2, opis="Transakcija U2")

    def test_user_sees_only_own_transactions_in_list(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("transaction_list"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Transakcija U1")
        self.assertNotContains(response, "Transakcija U2")

    def test_user_cannot_open_other_users_transaction_detail(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse("transaction_detail", kwargs={"pk": self.t2.pk}))
        self.assertEqual(response.status_code, 404)

    def test_user_sees_only_own_accounts(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("account_list"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Racun 1")
        self.assertNotContains(response, "Racun 2")

    def test_user_sees_only_own_categories(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("category_list"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Kategorija 1")
        self.assertNotContains(response, "Kategorija 2")


class TransactionCreateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="1234")
        self.acc = AccountFactory(user=self.user, naziv="Moj racun")
        self.cat = CategoryFactory(user=self.user, naziv="Moja kategorija")

    def test_create_transaction_sets_user(self):
        self.client.login(username="testuser", password="1234")

        url = reverse("transaction_create")
        payload = {
            "account": self.acc.pk,
            "category": self.cat.pk,
            "datum": "2026-02-21",
            "iznos": "10.00",
            "opis": "Nova transakcija",
        }

        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, 302)

        t = Transaction.objects.get(opis="Nova transakcija")
        self.assertEqual(t.user, self.user)
        self.assertEqual(t.account, self.acc)
        self.assertEqual(t.category, self.cat)