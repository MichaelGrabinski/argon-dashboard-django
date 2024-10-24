# Generated by Django 3.2.6 on 2024-07-24 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('available', 'Available'), ('in_use', 'In Use'), ('under_repair', 'Under Repair'), ('out_of_order', 'Out of Order')], default='available', max_length=20)),
                ('purchase_date', models.DateField(blank=True, null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=200, null=True)),
                ('model_number', models.CharField(blank=True, max_length=200, null=True)),
                ('assigned_to', models.CharField(blank=True, max_length=200, null=True)),
                ('location', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='tools_images/')),
            ],
        ),
    ]
