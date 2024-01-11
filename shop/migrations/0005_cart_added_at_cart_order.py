# Generated by Django 4.2.4 on 2023-08-14 07:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0004_alter_cart_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="added_at",
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 20, 0, 0)),
        ),
        migrations.AddField(
            model_name="cart",
            name="order",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
