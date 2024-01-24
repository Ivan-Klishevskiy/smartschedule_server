# Generated by Django 3.2.23 on 2024-01-19 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
