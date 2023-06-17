# Generated by Django 4.2 on 2023-06-03 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0004_alter_reservations_sport_hall_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservations',
            name='date_time_begin',
        ),
        migrations.RemoveField(
            model_name='reservations',
            name='date_time_end',
        ),
        migrations.AddField(
            model_name='reservations',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='reservations',
            name='time_from',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='reservations',
            name='time_to',
            field=models.TimeField(null=True),
        ),
    ]
