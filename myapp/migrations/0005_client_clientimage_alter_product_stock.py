# Generated by Django 4.1.3 on 2022-11-21 02:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_alter_order_status_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="clientImage",
            field=models.ImageField(blank=True, upload_to="clientImages/"),
        ),
        migrations.AlterField(
            model_name="product",
            name="stock",
            field=models.PositiveIntegerField(
                default=100,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(1000),
                ],
            ),
        ),
    ]
