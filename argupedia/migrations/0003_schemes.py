# Generated by Django 2.2.7 on 2019-11-24 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('argupedia', '0002_auto_20191122_2143'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schemes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheme_name', models.CharField(max_length=100)),
            ],
        ),
    ]
