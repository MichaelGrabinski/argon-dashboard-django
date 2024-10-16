# Generated by Django 4.2 on 2024-10-15 12:32

import apps.home.custom_storage
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_alter_invoice_valid_until_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='expense',
            name='project',
        ),
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='expense',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='valid_until',
            field=models.DateField(default=datetime.datetime(2024, 12, 14, 12, 32, 1, 166061)),
        ),
        migrations.AlterField(
            model_name='panorama',
            name='image',
            field=models.ImageField(storage=apps.home.custom_storage.StaticFileSystemStorage(), upload_to='tour_images/'),
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.category')),
            ],
        ),
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.category'),
        ),
    ]
