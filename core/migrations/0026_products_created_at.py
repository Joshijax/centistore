# Generated by Django 4.1.3 on 2023-02-23 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
