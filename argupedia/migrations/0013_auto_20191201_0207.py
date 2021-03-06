# Generated by Django 2.2.7 on 2019-12-01 02:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('argupedia', '0012_remove_entry_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schemestructure',
            name='is_conclusion',
        ),
        migrations.CreateModel(
            name='CriticalQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_attack_on_conclusion', models.BooleanField()),
                ('question', models.CharField(max_length=500)),
                ('related_scheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_scheme', to='argupedia.Scheme')),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='critical_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='critical_question', to='argupedia.CriticalQuestion'),
        ),
    ]
