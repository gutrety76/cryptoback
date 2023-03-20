from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Deposit(models.Model):
    user_id = models.IntegerField()
    crypto_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=100, decimal_places=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id)

class Notification(models.Model):
    user_id = models.IntegerField()
    message = models.CharField(max_length=300)

class Withdrawal(models.Model):
    user_id = models.IntegerField()
    crypto_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=100, decimal_places=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id)




class Exchange(models.Model):
    user_id = models.IntegerField()
    cryptoType_from = models.CharField(max_length=50)
    cryptoType_to = models.CharField(max_length=50)
    cryptoAmount_from = models.CharField(max_length=50)
    cryptoAmount_to = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id)


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    BTC = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])
    ETH = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])
    BNB = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])
    USDT = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])
    BUSD = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])
    ADA = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])
    XRP = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])
    SOL = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])
    DOGE = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])
    DOT = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])
    TRX = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])
    ETC = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])
    XLM = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])
    ATOM = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])
    NEAR = models.DecimalField(max_digits=100, decimal_places=10, default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.user.username
