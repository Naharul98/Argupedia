# Generated by Django 2.2.7 on 2019-11-24 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('argupedia', '0004_auto_20191124_1905'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchemeStructure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_in_school', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=50)),
                ('scheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheme', to='argupedia.Scheme')),
            ],
        ),
    ]
