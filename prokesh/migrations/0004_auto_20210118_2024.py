# Generated by Django 3.1.3 on 2021-01-18 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prokesh', '0003_auto_20210118_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workers',
            name='name',
            field=models.CharField(max_length=100, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='workers',
            name='url',
            field=models.SlugField(max_length=150, unique=True),
        ),
    ]
