# Generated by Django 5.0.1 on 2024-10-01 10:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_usersocialauth_user'),
        ('patron', '0004_alter_contributions_amount_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contributions',
            new_name='Payment',
        ),
        migrations.RenameModel(
            old_name='ContributionsUnauth',
            new_name='PaymentAnonymous',
        ),
    ]