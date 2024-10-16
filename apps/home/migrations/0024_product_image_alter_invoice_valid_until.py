# Generated by Django 4.2 on 2024-10-17 12:12

import apps.home.custom_storage
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_alter_invoice_valid_until'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=apps.home.custom_storage.StaticFileSystemStorage(), upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='valid_until',
            field=models.DateField(default=datetime.datetime(2024, 12, 16, 12, 12, 0, 902490)),
        ),
    ]
