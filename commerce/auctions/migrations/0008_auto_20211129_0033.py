# Generated by Django 3.2.9 on 2021-11-29 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_listing_watchers'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='starting',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.IntegerField(blank=True),
        ),
    ]