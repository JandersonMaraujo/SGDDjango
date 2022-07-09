# Generated by Django 3.2.13 on 2022-07-06 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sgdapi', '0010_alter_transaction_send_to_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='send_to_user',
            field=models.ForeignKey(default='janderson.araujo', on_delete=django.db.models.deletion.CASCADE, related_name='send_to_user', to='sgdapi.accountholder'),
            preserve_default=False,
        ),
    ]
