from django.contrib import admin
from .models import Wallet, Deposit, Exchange, Withdrawal

admin.site.register(Wallet)
admin.site.register(Deposit)
admin.site.register(Exchange)
admin.site.register(Withdrawal)
