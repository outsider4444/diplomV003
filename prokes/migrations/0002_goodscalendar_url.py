# Generated by Django 3.1.3 on 2021-02-15 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prokes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodscalendar',
            name='url',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
