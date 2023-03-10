# Generated by Django 3.2.14 on 2023-01-24 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_comment_id_alter_like_id_alter_post_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('published', 'published'), ('draft', 'draft')], default='published', max_length=50),
        ),
    ]
