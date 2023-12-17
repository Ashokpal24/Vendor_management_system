# Generated by Django 5.0 on 2023-12-17 16:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("POTracking", "0003_alter_purchaseorder_issue_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchaseorder",
            name="issue_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 12, 17, 16, 11, 34, 442999, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="order_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 12, 17, 16, 11, 34, 442874, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="quality_rating",
            field=models.FloatField(default=0.0),
        ),
    ]
