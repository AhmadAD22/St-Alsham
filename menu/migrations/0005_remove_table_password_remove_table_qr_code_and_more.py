# Generated by Django 5.0.2 on 2024-03-15 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='password',
        ),
        migrations.RemoveField(
            model_name='table',
            name='qr_code',
        ),
        migrations.AddField(
            model_name='table',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
