# Generated by Django 3.2 on 2021-05-27 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prokes', '0002_materialstorage_supplier_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsstorage',
            name='customer_checkout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prokes.checkoutgoods', verbose_name='Код заказа'),
        ),
        migrations.AlterField(
            model_name='goodsstorage',
            name='customer_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prokes.customer', verbose_name='Код заказчика'),
        ),
        migrations.AlterField(
            model_name='goodsstorage',
            name='goods_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prokes.goods', verbose_name='Код изделия'),
        ),
        migrations.AlterField(
            model_name='materialstorage',
            name='material_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prokes.materials', verbose_name='Код смеси'),
        ),
        migrations.AlterField(
            model_name='materialstorage',
            name='supplier_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prokes.suppliers', verbose_name='Код поставщика'),
        ),
        migrations.AlterField(
            model_name='nariad',
            name='goods_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prokes.goods', verbose_name='Код изделия'),
        ),
        migrations.AlterField(
            model_name='nariad',
            name='material_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prokes.materials', verbose_name='Код смеси'),
        ),
        migrations.AlterField(
            model_name='nariad',
            name='worker_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prokes.workers', verbose_name='Код сотрудника'),
        ),
        migrations.AlterField(
            model_name='otk',
            name='nariad_code',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='prokes.nariad', verbose_name='Код наряда'),
        ),
    ]
