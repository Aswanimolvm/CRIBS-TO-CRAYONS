# Generated by Django 3.2.24 on 2024-03-05 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baby_details',
            name='vaccination_id',
        ),
        migrations.RemoveField(
            model_name='baby_details',
            name='vaccination_status',
        ),
        migrations.RemoveField(
            model_name='vaccination',
            name='date',
        ),
        migrations.AddField(
            model_name='vaccination',
            name='duration',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='licence_proof',
            field=models.FileField(upload_to='licence'),
        ),
        migrations.CreateModel(
            name='Baby_vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccination_status', models.CharField(blank=True, max_length=50, null=True)),
                ('baby_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.baby_details')),
                ('vaccination_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.vaccination')),
            ],
        ),
    ]
