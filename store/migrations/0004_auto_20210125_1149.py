# Generated by Django 3.1.5 on 2021-01-25 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20210124_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addstore',
            name='quantityNo',
            field=models.FloatField(),
        ),
    ]
