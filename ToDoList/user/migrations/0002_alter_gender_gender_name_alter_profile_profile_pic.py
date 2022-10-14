# Generated by Django 4.1 on 2022-08-19 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gender',
            name='gender_name',
            field=models.CharField(max_length=50, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='profile_pics/default_profile', upload_to='', verbose_name='profile piture'),
        ),
    ]
