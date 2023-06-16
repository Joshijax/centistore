# Generated by Django 4.1.3 on 2023-06-16 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(blank=True, max_length=15)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.locationprice'),
        ),
    ]
