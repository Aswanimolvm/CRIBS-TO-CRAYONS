# Generated by Django 3.2.24 on 2024-03-25 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_baby_details_vaccination_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baby_details',
            name='vaccination_id',
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(auto_now=True)),
                ('Parent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.parent')),
                ('hospital_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.hospital')),
            ],
        ),
    ]
