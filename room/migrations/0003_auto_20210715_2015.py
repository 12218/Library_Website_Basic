# Generated by Django 3.2.5 on 2021-07-15 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_alter_room_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='room',
            name='start_time',
            field=models.TimeField(),
        ),
    ]