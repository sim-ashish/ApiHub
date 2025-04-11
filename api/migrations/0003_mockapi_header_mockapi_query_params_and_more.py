# Generated by Django 4.2.20 on 2025-04-11 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_mockapi'),
    ]

    operations = [
        migrations.AddField(
            model_name='mockapi',
            name='header',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AddField(
            model_name='mockapi',
            name='query_params',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AddField(
            model_name='mockapi',
            name='response_code',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='mockapi',
            name='response_msg',
            field=models.JSONField(null=True),
        ),
    ]
