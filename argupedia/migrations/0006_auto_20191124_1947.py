# Generated by Django 2.2.7 on 2019-11-24 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('argupedia', '0005_schemestructure'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schemestructure',
            old_name='year_in_school',
            new_name='ordering',
        ),
        migrations.AddField(
            model_name='schemestructure',
            name='section_title',
            field=models.CharField(default='sds', max_length=100),
            preserve_default=False,
        ),
    ]
