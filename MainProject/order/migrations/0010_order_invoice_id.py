# Generated by Django 5.0.3 on 2024-05-25 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_coupon_less_coupon_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='invoice_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
