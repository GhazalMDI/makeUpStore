# Generated by Django 5.0.3 on 2024-05-29 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_firstcategory_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='firstcategory',
            name='image',
        ),
        migrations.AddField(
            model_name='secondcategory',
            name='image',
            field=models.ImageField(null=True, upload_to='products/category/%Y/%M/%d'),
        ),
    ]