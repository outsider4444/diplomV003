from django.db import models
from datetime import datetime


# Create your models here.
from django.urls import reverse


def default_datetime():
    return datetime.now()


class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class UnitsMeasurement(models.Model):
    """Единицы измерения"""
    unit = models.CharField('Единица измерения', max_length=120)
    short_unit = models.CharField('Сокращение', max_length=10, default='')

    def __str__(self):
        return self.unit

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


class Workers(models.Model):
    """Сотрудники"""
    name = models.CharField('ФИО', max_length=100)
    email = models.EmailField('Email')
    birthday = models.DateField('Дата рождения')
    category = models.CharField('Категория', max_length=50)
    salary = models.PositiveIntegerField('Оклад', help_text='Вводить в рублях')
    url = models.SlugField(max_length=150, default='worker_', unique=True)
    # статус увольнения
    fired = models.BooleanField("Уволен", default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("worker_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class WorkTime(models.Model):
    """Время работы сотрудников"""
    worker_name = models.ForeignKey(Workers, verbose_name='Код сотрудника', on_delete=models.CASCADE)
    standard_time = models.IntegerField('Норма времени')
    done_time = models.IntegerField('Выполненное время')
    lose_time = models.IntegerField('Пропущенно времени')
    date_vacation = models.DateField('Дата отпуска')

    def __str__(self):
        return str(self.worker_name)

    class Meta:
        verbose_name = 'Время работы сотрудника'
        verbose_name_plural = 'Время работы сотрудников'


class Smesi(models.Model):
    """Смеси"""
    code = models.CharField('Код', max_length=120, primary_key=True)
    value = models.PositiveSmallIntegerField('Количество')
    weight = models.FloatField('Вес')
    date = models.DateField('Дата изготовления', default=default_datetime)
    valid = models.DateField('Годен до')
    # протестировать
    worker_name = models.ManyToManyField(Workers, verbose_name='ФИО сотрудника')
    url = models.SlugField(max_length=150, default='smesi_', unique=True)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("smesi_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = 'Смесь'
        verbose_name_plural = 'Смеси'


class Goods(models.Model):
    """Изделия"""
    code = models.CharField('Код изделия', max_length=120, primary_key=True)
    cleaning_period = models.FloatField('Период чистки')
    number_nest = models.FloatField('Номер гнезда')
    # изменить позже
    percent_mass = models.IntegerField('Процент массы')
    weight_clean = models.FloatField('Вес чистой детали')
    norma_with_carpet = models.IntegerField('Норма с ковром')
    consumption_smesi = models.IntegerField('Расход смеси')
    one_person_norma = models.IntegerField('Норма на одного человека')
    two_person_norma = models.IntegerField('Норма на двух чловек')
    defect_limit = models.FloatField('Лимит брака')
    # сделать среднее значение
    min_temperature = models.IntegerField('Минимальная температура')
    max_temperature = models.IntegerField('Максимальная температура')
    min_malt = models.IntegerField('Минимальная выдержка')
    max_malt = models.IntegerField('Максимальная выдержка')
    min_pressure = models.IntegerField('Минимальное давление')
    max_pressure = models.IntegerField('Максимальное давление')
    min_strength = models.IntegerField('Минимальная твердость')
    max_strength = models.IntegerField('Максимальная твердость')
    measurement = models.ManyToManyField(UnitsMeasurement, verbose_name='Единицы измерения')
    url = models.SlugField(max_length=150, default='goods_', unique=True)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("goods_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'


class Remote(models.Model):
    """Списанные смеси и изделия"""
    code_smesi = models.ManyToManyField(Smesi, verbose_name='Код смеси')
    delete_date = models.DateField('Дата списания', default=default_datetime)
    name = models.CharField('Название', max_length=120)
    code_goods = models.ManyToManyField(Goods, verbose_name='Код изделия')
    value = models.IntegerField('Количество')
    norma = models.IntegerField('Норма')
    scrap_materials = models.IntegerField('Брак сырья')
    costs_material = models.IntegerField('Затраты сырья')
    measurement = models.ManyToManyField(UnitsMeasurement, verbose_name='Единицы измерения')
    url = models.SlugField(max_length=150, default='remote_', unique=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Списанное'
        verbose_name_plural = 'Списанные'


class Suppliers(models.Model):
    """Поставщики"""
    # изменить
    name = models.CharField('Имя поставщика', max_length=120)
    email = models.EmailField('Email', unique=True)
    code_smesi = models.ManyToManyField(Smesi, verbose_name='Код смеси')
    value = models.PositiveSmallIntegerField('Количество')
    date = models.DateField('Дата поставки', default=default_datetime)
    url = models.SlugField(max_length=150, default='supplier_', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Customers(models.Model):
    """Заказчики"""
    name = models.CharField('Имя заказчика', max_length=120)
    email = models.EmailField('Email', unique=True)
    date = models.DateField('Дата заказа', default=default_datetime)
    code_goods = models.ManyToManyField(Goods, verbose_name='Код изделия')
    values = models.IntegerField('Количество')
    url = models.SlugField(max_length=150, default='customer_', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'
