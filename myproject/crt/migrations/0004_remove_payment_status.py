# Generated by Django 4.1.5 on 2023-01-13 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crt', '0003_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='status',
        ),
    ]