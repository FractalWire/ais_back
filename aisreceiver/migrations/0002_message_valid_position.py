# Generated by Django 2.2.4 on 2019-08-26 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aisreceiver', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='valid_position',
            field=models.BooleanField(default=True),
        ),
    ]
