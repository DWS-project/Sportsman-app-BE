# Generated by Django 4.2.1 on 2023-06-06 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0017_alter_owner_picture_alter_user_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitations',
            name='type',
            field=models.CharField(default='Permanent Team', max_length=20),
        ),
    ]
