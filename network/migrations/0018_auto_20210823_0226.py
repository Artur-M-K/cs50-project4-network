# Generated by Django 3.1.7 on 2021-08-23 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0017_auto_20210823_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='isLiked',
            field=models.BooleanField(),
        ),
    ]
