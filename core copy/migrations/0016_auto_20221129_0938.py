# Generated by Django 2.2.14 on 2022-11-29 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20221128_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub_category',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_cat', to='core.Category'),
        ),
    ]