# Generated by Django 4.2.20 on 2025-04-02 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='endpoint_url',
            field=models.CharField(max_length=250),
        ),
    ]
