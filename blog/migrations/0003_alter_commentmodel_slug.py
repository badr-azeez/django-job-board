# Generated by Django 5.0.4 on 2024-07-07 18:00

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blogmodel_full_text_alter_commentmodel_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='slug',
            field=autoslug.fields.AutoSlugField(allow_unicode=True, editable=False, populate_from='random_id', primary_key=True, serialize=False, unique=True),
        ),
    ]
