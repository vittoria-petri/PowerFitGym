# Generated by Django 4.2.2 on 2023-06-07 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userassign',
            old_name='AsForm',
            new_name='Scheda',
        ),
    ]
