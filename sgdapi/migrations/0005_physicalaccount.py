# Generated by Django 3.2.16 on 2024-01-17 01:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sgdapi', '0004_auto_20231118_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhysicalAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('initials', models.CharField(max_length=15)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('virtual_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgdapi.account')),
            ],
        ),
    ]
