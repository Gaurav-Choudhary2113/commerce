# Generated by Django 4.1.7 on 2023-05-18 10:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0007_listing_created_on"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="watchers",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="watch_products",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
