# Generated by Django 5.0.6 on 2024-06-07 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planetarium_api', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planetariumdome',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
