# Generated by Django 2.2.7 on 2019-11-24 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('argupedia', '0006_auto_20191124_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='schemestructure',
            name='is_conclusion',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
