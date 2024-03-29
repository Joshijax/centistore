# Generated by Django 4.1.3 on 2023-05-28 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('DS', 'Dispatched'), ('IT', 'In transit'), ('DL', 'Delivered'), ('PR', 'Processing'), ('CL', 'Cancelled')], default='PR', max_length=3),
        ),
    ]
