# Generated by Django 5.0.3 on 2024-05-13 11:48

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_variant'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tag',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
