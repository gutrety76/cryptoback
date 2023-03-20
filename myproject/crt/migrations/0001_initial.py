# Generated by Django 4.1.5 on 2023-01-12 08:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('crypto_type', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=10, max_digits=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('crypto_type', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=10, max_digits=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BTC', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('ETH', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('BNB', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('USDT', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('BUSD', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('ADA', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('XRP', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('SOL', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('DOGE', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('DOT', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('TRX', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('ETC', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('XLM', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('ATOM', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('NEAR', models.DecimalField(decimal_places=10, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cryptoType_from', models.CharField(max_length=50)),
                ('cryptoType_to', models.CharField(max_length=50)),
                ('cryptoAmount_from', models.CharField(max_length=50)),
                ('cryptoAmount_to', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
