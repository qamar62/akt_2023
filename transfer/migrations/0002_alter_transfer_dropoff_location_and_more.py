# Generated by Django 4.0.2 on 2022-07-08 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='dropoff_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transfer.dropofflocation'),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='pickup_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transfer.pickuplocation'),
        ),
    ]
