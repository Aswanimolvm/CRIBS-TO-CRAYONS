# Generated by Django 3.2.24 on 2024-04-23 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_vaccineupdationrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vaccinedocument',
            name='baby_id',
        ),
        migrations.AddField(
            model_name='vaccinedocument',
            name='parent_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app1.parent'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='vaccineUpdationRequest',
        ),
    ]
