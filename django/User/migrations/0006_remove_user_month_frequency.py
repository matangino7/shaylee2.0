# Generated by Django 4.2.4 on 2023-12-28 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_alter_user_off_day1_alter_user_off_day2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='month_frequency',
        ),
    ]
