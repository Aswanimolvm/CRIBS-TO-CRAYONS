# Generated by Django 3.2.24 on 2024-04-08 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_doctor_main_slot'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='consulting_time',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
