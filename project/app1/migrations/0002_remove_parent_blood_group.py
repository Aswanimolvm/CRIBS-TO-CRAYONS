# Generated by Django 3.2.24 on 2024-04-19 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='blood_group',
        ),
    ]
