# Generated by Django 3.2.13 on 2022-06-18 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgdapi', '0005_accountholder_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountholder',
            name='prof_pic',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]
