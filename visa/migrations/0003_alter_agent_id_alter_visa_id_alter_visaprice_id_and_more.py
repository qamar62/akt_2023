# Generated by Django 4.0.2 on 2022-06-10 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visa', '0002_alter_visa_options_alter_agent_agent_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='visa',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='visaprice',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='visatype',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
