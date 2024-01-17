# Generated by Django 3.2.16 on 2023-11-18 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgdapi', '0003_auto_20221231_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initiated_by', models.JSONField()),
                ('before', models.JSONField()),
                ('after', models.JSONField()),
                ('event', models.CharField(max_length=50)),
                ('ip', models.GenericIPAddressField()),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=19),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='balance',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=19),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='credit',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
