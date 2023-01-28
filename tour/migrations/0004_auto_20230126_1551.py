# Generated by Django 3.2.14 on 2023-01-26 11:51

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tour', '0003_auto_20220805_1203'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewrating',
            old_name='product',
            new_name='tour',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='adult_price',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='child_price',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='infant_price',
        ),
        migrations.AddField(
            model_name='tour',
            name='user_wishlist',
            field=models.ManyToManyField(blank=True, related_name='user_twishlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tour',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, help_text='Description of tour', null=True),
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult_price', models.FloatField()),
                ('child_price', models.FloatField()),
                ('infant_price', models.FloatField()),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price', to='tour.tour')),
            ],
        ),
    ]