# Generated by Django 4.1.3 on 2023-06-20 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_locationprice_order_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationprice',
            name='state',
            field=models.CharField(max_length=1000),
        ),
    ]
