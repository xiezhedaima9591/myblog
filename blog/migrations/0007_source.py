# Generated by Django 2.1.2 on 2018-11-06 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20181106_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.Post')),
                ('share_url', models.URLField(blank=True, null=True, verbose_name='资源下载链接')),
            ],
            options={
                'verbose_name': '资源分享',
                'verbose_name_plural': '资源分享',
                'ordering': ['-create_time'],
            },
            bases=('blog.post',),
        ),
    ]
