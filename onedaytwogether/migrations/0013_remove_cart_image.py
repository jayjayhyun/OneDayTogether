# Generated by Django 4.2.2 on 2023-09-08 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onedaytwogether', '0012_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='Image',
        ),
    ]
