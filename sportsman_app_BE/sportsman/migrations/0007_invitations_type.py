# Generated by Django 4.2 on 2023-06-04 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0006_permanentteams_team_name_alter_reservations_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitations',
            name='type',
            field=models.CharField(default='Permanent Team', max_length=20),
        ),
    ]