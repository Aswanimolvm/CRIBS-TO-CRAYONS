# Generated by Django 3.2.24 on 2024-04-23 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_auto_20240422_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('street', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('pincode', models.IntegerField()),
                ('Email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('login_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='seller',
            name='login_id',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='customer_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='customer_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='seller_id',
        ),
        migrations.RemoveField(
            model_name='productbooking',
            name='customer_id',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Seller',
        ),
        migrations.AddField(
            model_name='cart',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.user'),
        ),
        migrations.AddField(
            model_name='product',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.user'),
        ),
        migrations.AddField(
            model_name='productbooking',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.user'),
        ),
    ]
