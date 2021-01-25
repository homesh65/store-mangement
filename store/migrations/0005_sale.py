# Generated by Django 3.1.5 on 2021-01-25 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20210125_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soldquantity', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('item', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.addstore')),
            ],
        ),
    ]