# Generated by Django 3.2.14 on 2022-08-05 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0002_alter_category_id_alter_excl_id_alter_extra_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excl',
            name='tour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='excludes', to='tour.tour'),
        ),
        migrations.AlterField(
            model_name='inclusions',
            name='tour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='includes', to='tour.tour'),
        ),
        migrations.AlterField(
            model_name='tourgallery',
            name='tour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='tour.tour'),
        ),
    ]