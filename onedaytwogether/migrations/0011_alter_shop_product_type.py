# Generated by Django 4.2.2 on 2023-09-07 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onedaytwogether', '0010_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='Product_Type',
            field=models.CharField(choices=[('Equipment', 'Equipment'), ('Tents', 'Tents'), ('Equipment', 'Equipment'), ('Bags', 'Bags'), ('Clothes', 'Clothes'), ('Shoes', 'Shoes'), ('Accessory', 'Accessory'), ('Shelters', 'Shelters')], max_length=30),
        ),
    ]
