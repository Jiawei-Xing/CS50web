# Generated by Django 3.2.9 on 2021-11-28 23:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20211128_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchers',
            field=models.ManyToManyField(blank=True, related_name='watch_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
