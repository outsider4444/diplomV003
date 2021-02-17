from django.db import models
from datetime import datetime

# Create your models here.
from django.urls import reverse


def default_datetime():
    return datetime.now()


class UnitsMeasurement(models.Model):
    short_unit = models.CharField('Единица измерения', max_length=10)
    url = models.SlugField(max_length=150, default='unit_', unique=True)

    def __str__(self):
        return self.short_unit

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


class Goods(models.Model):
    """Изделия"""
    code = models.CharField('Код изделия', max_length=120, primary_key=True)
    # сделать фото необязательным
    image = models.ImageField("Фотография изделия", upload_to="goods/", blank=True)
    # изменить позже
    weight_clean = models.FloatField('Вес чистой детали', default=0)
    norma_with_carpet = models.IntegerField('Норма с ковром', default=0)
    consumption_smesi = models.IntegerField('Расход смеси', default=0)
    one_person_norma = models.IntegerField('Норма на одного человека', default=0)
    two_person_norma = models.IntegerField('Норма на двух чловек', default=0)
    defect_limit = models.FloatField('Лимит брака', default=0)
    # сделать среднее значение
    min_temperature = models.IntegerField('Минимальная температура', default=0)
    max_temperature = models.IntegerField('Максимальная температура', default=0)
    min_malt = models.IntegerField('Минимальная выдержка', default=0)
    max_malt = models.IntegerField('Максимальная выдержка', default=0)
    min_pressure = models.IntegerField('Минимальное давление', default=0)
    max_pressure = models.IntegerField('Максимальное давление', default=0)
    min_strength = models.IntegerField('Минимальная твердость', default=0)
    max_strength = models.IntegerField('Максимальная твердость', default=0)
    measurement = models.ForeignKey(UnitsMeasurement, verbose_name='Единицы измерения',
                                    on_delete=models.PROTECT)
    # worker_name = models.OneToOneField(Workers, verbose_name='ФИО сотрудника', on_delete=models.PROTECT)
    url = models.SlugField(max_length=150, default='goods_', unique=True)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("goods_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'


class GoodsForm(models.Model):
    """Формы деталей"""
    code_goods = models.ForeignKey(Goods, verbose_name="Код изделия", on_delete=models.PROTECT)
    duplicate = models.CharField("Название(дубликат)", max_length=150)
    cleaning_period = models.FloatField("Период чистки")
    number_nest = models.FloatField("Номер гнезда")
    percent_mass = models.IntegerField("Процент массы")
    url = models.SlugField(max_length=150, blank=True)

    def __str__(self):
        return self.code_goods

    def get_absolute_url(self):
        return reverse("goods_form", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Форма изделия"
        verbose_name_plural = "Формы изделий"


class GoodsCalendar(models.Model):
    """Календарь создания изделий"""
    code_goods = models.ForeignKey(Goods, verbose_name="Код изделия", on_delete=models.CASCADE)
    month = models.DateField("Месяц", help_text="Вписывать только месяц и год, день оставлть '01' ")
    lith = models.IntegerField("Отлито шт.")
    remote = models.IntegerField("Брак шт.")
    # добавить в процентах вычисляемое поле
    remote_percent = models.FloatField("Брак %")
    ###
    one_man_sr = models.CharField("Смена выработки на 1 человека в СРЕДНЕМ", max_length=150)
    one_man_max = models.CharField("Смена выработки на 1 человека МАКСИМАЛЬНО", max_length=150)
    two_man_sr = models.CharField("Смена выработки на 2 человек в СРЕДНЕМ", max_length=150)
    two_man_max = models.CharField("Смена выработки на 2 человека МАКСИМАЛЬНО", max_length=150)

    def __str__(self):
        return str(self.month)

    class Meta:
        verbose_name = "Календарь изделий"
        verbose_name_plural = "Календарь изделий"
