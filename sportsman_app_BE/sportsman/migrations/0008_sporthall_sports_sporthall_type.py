# Generated by Django 4.2 on 2023-05-20 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0007_user_access_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='sporthall',
            name='sports',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='sporthall',
            name='type',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
