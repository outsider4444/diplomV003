# Generated by Django 3.1.3 on 2021-01-28 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prokesh', '0004_auto_20210128_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workers',
            name='photo',
            field=models.ImageField(upload_to='workers/', verbose_name='Фотография сотрудника'),
        ),
    ]
