# Generated by Django 2.2.27 on 2022-04-18 11:37

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_auto_20220418_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='profile_pic',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='a35780aa-90d8-4311-bf37-d12479764254.jpeg', force_format=None, keep_meta=True, null=True, quality=100, size=[50, 80], upload_to='authors'),
        ),
    ]