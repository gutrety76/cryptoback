# Generated by Django 4.1.5 on 2023-01-13 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crt', '0002_remove_exchange_user_exchange_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('currency', models.CharField(max_length=3)),
                ('status', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.IntegerField()),
            ],
        ),
    ]