# Generated by Django 2.1.2 on 2018-11-05 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_time'], 'verbose_name': '文章评论', 'verbose_name_plural': '文章评论'},
        ),
    ]
