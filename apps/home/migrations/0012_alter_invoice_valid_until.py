# Generated by Django 4.2 on 2024-10-08 14:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_unit_tour_image_alter_invoice_valid_until'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='valid_until',
            field=models.DateField(default=datetime.datetime(2024, 12, 7, 14, 58, 27, 313819)),
        ),
    ]
