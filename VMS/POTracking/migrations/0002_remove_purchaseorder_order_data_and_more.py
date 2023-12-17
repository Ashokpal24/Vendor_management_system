# Generated by Django 5.0 on 2023-12-17 15:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("POTracking", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="purchaseorder",
            name="order_data",
        ),
        migrations.AddField(
            model_name="purchaseorder",
            name="order_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 12, 17, 15, 22, 15, 67369)
            ),
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="issue_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 12, 17, 15, 22, 15, 67476)
            ),
        ),
    ]