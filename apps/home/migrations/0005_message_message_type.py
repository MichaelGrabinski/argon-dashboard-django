# Generated by Django 4.2 on 2024-09-16 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_conversation_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_type',
            field=models.CharField(choices=[('text', 'Text'), ('image', 'Image'), ('audio', 'Audio')], default='text', max_length=10),
        ),
    ]
