# Generated by Django 4.1.3 on 2023-05-27 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_remove_orderitem_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('DS', 'Dispatched'), ('IT', 'In transit'), ('DL', 'Delivered'), ('DSO', 'Dispatching soon'), ('PR', 'Processing'), ('CL', 'Cancelled')], default='PR', max_length=3),
        ),
    ]
