# Generated by Django 3.2 on 2021-05-28 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prokes', '0003_auto_20210528_0100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workers',
            name='fired',
        ),
        migrations.AlterField(
            model_name='checkoutgoods',
            name='code_goods',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prokes.goods', verbose_name='Код изделия'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(default='8', max_length=11, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='deliveriesmaterials',
            name='code_material',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prokes.materials', verbose_name='Код смеси'),
        ),
        migrations.AlterField(
            model_name='goodsstorage',
            name='customer_checkout',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prokes.checkoutgoods', verbose_name='Код заказа'),
        ),
        migrations.AlterField(
            model_name='goodsstorage',
            name='customer_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prokes.customer', verbose_name='Код заказчика'),
        ),
        migrations.AlterField(
            model_name='materials',
            name='code',
            field=models.CharField(max_length=120, verbose_name='Код материала'),
        ),
        migrations.AlterField(
            model_name='materialstorage',
            name='supplier_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prokes.suppliers', verbose_name='Код поставщика'),
        ),
        migrations.AlterField(
            model_name='nariad',
            name='goods_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prokes.goods', verbose_name='Код изделия'),
        ),
        migrations.AlterField(
            model_name='nariad',
            name='material_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prokes.materials', verbose_name='Код материала'),
        ),
        migrations.AlterField(
            model_name='nariad',
            name='worker_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prokes.workers', verbose_name='Код сотрудника'),
        ),
        migrations.AlterField(
            model_name='suppliers',
            name='phone_number',
            field=models.CharField(default='8', max_length=11, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='workers',
            name='phone_number',
            field=models.CharField(default='8', max_length=11, verbose_name='Номер телефона'),
        ),
    ]
