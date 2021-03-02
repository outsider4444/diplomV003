# Generated by Django 3.1.3 on 2021-03-02 19:33

from django.db import migrations, models
import django.db.models.deletion
import prokes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Имя заказчика')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Номер телефона')),
                ('representative', models.CharField(max_length=100, verbose_name='Представитель (ФИО)')),
            ],
            options={
                'verbose_name': 'Заказчик',
                'verbose_name_plural': 'Заказчики',
            },
        ),
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
            name='Workers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Код сотрудника')),
                ('name', models.CharField(max_length=100, verbose_name='ФИО')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('category', models.CharField(max_length=50, verbose_name='Категория')),
                ('salary', models.PositiveIntegerField(help_text='Вводить в рублях', verbose_name='Оклад')),
                ('standard_time', models.IntegerField(verbose_name='Норма времени')),
                ('lose_time', models.IntegerField(verbose_name='Пропущенно времени')),
                ('cof_proisvod', models.IntegerField(help_text='Указывать в процентах', verbose_name='Коэфициент производительности')),
                ('fired', models.BooleanField(default=False, verbose_name='Уволен')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='GoodsDefaultForm',
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
        migrations.CreateModel(
            name='CheckoutGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=prokes.models.default_datetime, verbose_name='Дата заказа')),
                ('order', models.TextField(verbose_name='Заказ')),
                ('values', models.IntegerField(verbose_name='Количество')),
                ('code_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prokes.goods', verbose_name='Код изделия')),
                ('customer_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prokes.customer', verbose_name='Имя заказчика')),
            ],
            options={
                'verbose_name': 'Дата заказа',
                'verbose_name_plural': 'Даты заказов',
            },
        ),
    ]
