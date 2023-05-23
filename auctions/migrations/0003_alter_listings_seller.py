# Generated by Django 4.1.7 on 2023-05-17 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_bids_comments_listings"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listings",
            name="seller",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="seller",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
