# Generated by Django 4.2.12 on 2024-05-14 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_v2', '0003_alter_message_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='command',
            field=models.CharField(default='blank', max_length=256),
        ),
    ]
