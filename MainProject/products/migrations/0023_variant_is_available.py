# Generated by Django 5.0.3 on 2024-05-25 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_alter_variant_discount_alter_variant_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]