# Generated by Django 3.1.1 on 2020-09-30 10:49

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20200930_0716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='features',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
