# Generated by Django 4.1.3 on 2023-02-24 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('DS', 'Dispatched'), ('IT', 'In transit'), ('DL', 'Delivered'), ('DSO', 'Dispatching soon'), ('CL', 'Cancelled')], default='DSO', max_length=3),
        ),
    ]
