# Generated by Django 4.2 on 2024-10-08 11:56

import apps.home.custom_storage
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_remove_service_labor_entries_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='tour_image',
            field=models.ImageField(blank=True, null=True, storage=apps.home.custom_storage.StaticFileSystemStorage(), upload_to='tour_images/'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='valid_until',
            field=models.DateField(default=datetime.datetime(2024, 12, 7, 11, 56, 19, 592259)),
        ),
    ]