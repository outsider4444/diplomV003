# Generated by Django 3.1.3 on 2021-01-22 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prokesh', '0011_auto_20210122_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='measurement',
        ),
    ]
