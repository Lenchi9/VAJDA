from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('TEKUCI', 'Tekući račun'),
        ('STEDNJA', 'Štednja'),
        ('KES', 'Gotovina'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    naziv = models.CharField(max_length=100)
    tip = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    pocetno_stanje = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.naziv} ({self.tip})"


class Category(models.Model):
    CATEGORY_TYPES = [
        ('PRIHOD', 'Prihod'),
        ('RASHOD', 'Rashod'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    naziv = models.CharField(max_length=100)
    tip = models.CharField(max_length=20, choices=CATEGORY_TYPES)

    def __str__(self):
        return self.naziv


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    datum = models.DateField()
    iznos = models.DecimalField(max_digits=10, decimal_places=2)
    opis = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.datum} - {self.iznos} €"