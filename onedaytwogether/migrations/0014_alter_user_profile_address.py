# Generated by Django 4.2.2 on 2023-09-09 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onedaytwogether', '0013_remove_cart_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='Address',
            field=models.CharField(max_length=1000),
        ),
    ]
