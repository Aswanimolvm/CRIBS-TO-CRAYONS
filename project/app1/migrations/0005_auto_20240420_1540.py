# Generated by Django 3.2.24 on 2024-04-20 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_auto_20240420_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbooking',
            name='parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.parent'),
        ),
        migrations.AlterField(
            model_name='productbooking',
            name='customer_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.customer'),
        ),
    ]
