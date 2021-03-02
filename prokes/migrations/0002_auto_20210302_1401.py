# Generated by Django 3.1.3 on 2021-03-02 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prokes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkoutgoods',
            name='code_goods',
        ),
        migrations.AddField(
            model_name='checkoutgoods',
            name='code_goods',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='prokes.goods', verbose_name='Код изделия'),
            preserve_default=False,
        ),
    ]
