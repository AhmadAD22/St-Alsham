# Generated by Django 5.0.2 on 2024-03-25 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_order_orderitem_order_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='performed',
            field=models.BooleanField(default=False),
        ),
    ]
