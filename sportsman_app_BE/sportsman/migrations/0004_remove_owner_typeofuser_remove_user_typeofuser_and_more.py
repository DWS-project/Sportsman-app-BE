# Generated by Django 4.2 on 2023-05-09 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0003_owner_team_user_age_user_city_user_interests_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='typeOfUser',
        ),
        migrations.RemoveField(
            model_name='user',
            name='typeOfUser',
        ),
        migrations.AlterField(
            model_name='owner',
            name='type',
            field=models.CharField(max_length=10, null=True),
        ),
    ]