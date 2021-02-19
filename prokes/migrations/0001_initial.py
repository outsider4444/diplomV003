# Generated by Django 3.1.3 on 2021-02-19 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=120, verbose_name='Код изделия')),
                ('image', models.ImageField(blank=True, upload_to='goods/', verbose_name='Фотография изделия')),
                ('weight_clean', models.FloatField(default=0, verbose_name='Вес чистой детали')),
                ('norma_with_carpet', models.IntegerField(default=0, verbose_name='Норма с ковром')),
                ('consumption_smesi', models.IntegerField(default=0, verbose_name='Расход смеси')),
                ('one_person_norma', models.IntegerField(default=0, verbose_name='Норма на одного человека')),
                ('defect_limit', models.FloatField(default=0, verbose_name='Лимит брака')),
            ],
            options={
                'verbose_name': 'Изделие',
                'verbose_name_plural': 'Изделия',
            },
        ),
        migrations.CreateModel(
            name='GoodsForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duplicate', models.CharField(max_length=150, verbose_name='Название(дубликат)')),
                ('cleaning_period', models.FloatField(verbose_name='Период чистки')),
                ('number_nest', models.FloatField(verbose_name='Номер гнезда')),
                ('percent_mass', models.IntegerField(verbose_name='Процент массы')),
                ('code_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prokes.goods', verbose_name='Код изделия')),
            ],
            options={
                'verbose_name': 'Форма изделия',
                'verbose_name_plural': 'Формы изделий',
            },
        ),
        migrations.CreateModel(
            name='GoodsCalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField(help_text="Вписывать только месяц и год, день оставлть '01' ", verbose_name='Месяц')),
                ('lith', models.IntegerField(verbose_name='Отлито шт.')),
                ('remote', models.IntegerField(verbose_name='Брак шт.')),
                ('remote_percent', models.FloatField(verbose_name='Брак %')),
                ('one_man_sr', models.CharField(max_length=150, verbose_name='Смена выработки на 1 человека в СРЕДНЕМ')),
                ('one_man_max', models.CharField(max_length=150, verbose_name='Смена выработки на 1 человека МАКСИМАЛЬНО')),
                ('two_man_sr', models.CharField(max_length=150, verbose_name='Смена выработки на 2 человек в СРЕДНЕМ')),
                ('two_man_max', models.CharField(max_length=150, verbose_name='Смена выработки на 2 человека МАКСИМАЛЬНО')),
                ('code_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prokes.goods', verbose_name='Код изделия')),
            ],
            options={
                'verbose_name': 'Календарь изделий',
                'verbose_name_plural': 'Календарь изделий',
            },
        ),
    ]
