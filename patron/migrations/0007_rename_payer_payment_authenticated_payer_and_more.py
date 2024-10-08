# Generated by Django 5.0.1 on 2024-10-01 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0006_alter_paymentanonymous_payer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='payer',
            new_name='authenticated_payer',
        ),
        migrations.AddField(
            model_name='payment',
            name='anonymous_payer',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.DeleteModel(
            name='PaymentAnonymous',
        ),
    ]
