# Generated by Django 3.1.3 on 2020-11-07 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auction_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='img',
            field=models.ImageField(upload_to=''),
        ),
    ]
