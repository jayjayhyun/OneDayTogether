# Generated by Django 4.2.2 on 2023-09-03 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onedaytwogether', '0008_alter_user_profile_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
