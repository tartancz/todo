# Generated by Django 4.1 on 2022-08-23 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_profile_delete_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='delete_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
