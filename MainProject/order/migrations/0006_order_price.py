# Generated by Django 5.0.3 on 2024-05-24 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_order_buy_order_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.PositiveIntegerField(null=True),
        ),
    ]