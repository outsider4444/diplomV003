# Generated by Django 3.1.3 on 2021-02-23 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prokes', '0002_auto_20210223_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutgoods',
            name='code_goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prokes.goods', verbose_name='Код изделия'),
        ),
    ]
