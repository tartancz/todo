# Generated by Django 4.1 on 2022-10-04 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_profile_delete_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gender',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['id']},
        ),
    ]
