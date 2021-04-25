from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model


class User(AbstractUser):
    capital = models.IntegerField(default=0)
    total_invested = models.IntegerField(default=0)
    total_sold = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} has {self.capital} available to invest"


class Stocks(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stocks_owned")
    ticker = models.CharField(max_length=10)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.owner.username} has {self.quantity} stocks of {self.ticker}"


class Transaction(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions")
    ticker = models.CharField(max_length=10)
    quantity = models.IntegerField(default=0)
    sum = models.IntegerField(default=0)

    def __str__(self):
        if self.quantity > 0:
            return f"{self.owner.username} bought {self.quantity} stocks of {self.ticker} for {self.sum}"
        return f"{self.owner.username} sold {-self.quantity} stocks of {self.ticker} for {self.sum}"
