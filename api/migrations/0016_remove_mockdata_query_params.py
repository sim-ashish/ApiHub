# Generated by Django 4.2.20 on 2025-04-15 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_mockdata_query_params'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mockdata',
            name='query_params',
        ),
    ]
