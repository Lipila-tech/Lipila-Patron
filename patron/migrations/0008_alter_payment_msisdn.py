# Generated by Django 5.0.1 on 2024-10-05 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0007_rename_payer_payment_authenticated_payer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='msisdn',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
