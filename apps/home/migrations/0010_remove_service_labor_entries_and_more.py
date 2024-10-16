# Generated by Django 4.2 on 2024-10-07 11:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_invoice_alter_projectattachment_project_service_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='labor_entries',
        ),
        migrations.RemoveField(
            model_name='service',
            name='materials',
        ),
        migrations.RemoveField(
            model_name='service',
            name='project',
        ),
        migrations.RemoveField(
            model_name='service',
            name='unit',
        ),
        migrations.AddField(
            model_name='lineitem',
            name='labor_cost',
            field=models.DecimalField(decimal_places=2, default=1, editable=False, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lineitem',
            name='materials_cost',
            field=models.DecimalField(decimal_places=2, default=1, editable=False, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lineitem',
            name='overhead',
            field=models.DecimalField(decimal_places=2, default=1, editable=False, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lineitem',
            name='profit',
            field=models.DecimalField(decimal_places=2, default=1, editable=False, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='labor_cost_per_unit',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='material_cost_per_unit',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='minimum_charge',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='service',
            name='overhead_percentage',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=5),
        ),
        migrations.AddField(
            model_name='service',
            name='profit_percentage',
            field=models.DecimalField(decimal_places=2, default=15, max_digits=5),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='valid_until',
            field=models.DateField(default=datetime.datetime(2024, 12, 6, 11, 39, 27, 166062)),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='quantity',
            field=models.DecimalField(decimal_places=2, help_text='Area in square feet', max_digits=10),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(),
        ),
    ]
