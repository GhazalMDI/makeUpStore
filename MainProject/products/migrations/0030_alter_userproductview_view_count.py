# Generated by Django 5.0.3 on 2024-05-29 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_userproductview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproductview',
            name='view_count',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
