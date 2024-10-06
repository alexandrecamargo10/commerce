# Generated by Django 5.0.7 on 2024-09-15 14:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='userId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
