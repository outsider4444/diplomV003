from django.db import models
from datetime import datetime

# Create your models here.


def default_datetime():
    return datetime.now()


class Workers(models.Model):
    """Сотрудники"""
    code = models.CharField('Код сотрудника', max_length=100, unique=True)
    name = models.CharField('ФИО', max_length=100)
    email = models.EmailField('Email')
    birthday = models.DateField('Дата рождения')
    category = models.CharField('Категория', max_length=50)
    salary = models.PositiveIntegerField('Оклад', help_text='Вводить в рублях')
    standard_time = models.IntegerField('Норма времени')
    lose_time = models.IntegerField('Пропущенно времени')
    cof_proisvod = models.IntegerField('Коэфициент производительности', help_text='Указывать в процентах')
    # статус увольнения
    fired = models.BooleanField("Уволен", default=False)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Goods(models.Model):
    """Изделия"""
    code = models.CharField('Код изделия', max_length=120)
    image = models.ImageField("Фотография изделия", upload_to="goods/", blank=True)
    # изменить позже
    weight_clean = models.FloatField('Вес чистой детали', default=0)
    norma_with_carpet = models.IntegerField('Норма с ковром', default=0)
    consumption_smesi = models.IntegerField('Расход смеси', default=0)
    one_person_norma = models.IntegerField('Норма на одного человека', default=0)
    defect_limit = models.FloatField('Лимит брака', default=0)
    # worker_name = models.OneToOneField(Workers, verbose_name='ФИО сотрудника', on_delete=models.PROTECT)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'


class GoodsDefaultForm(models.Model):
    """Формы деталей"""
    code_goods = models.ForeignKey(Goods, verbose_name="Код изделия", on_delete=models.CASCADE)
    duplicate = models.CharField("Название(дубликат)", max_length=150)
    cleaning_period = models.FloatField("Период чистки")
    number_nest = models.FloatField("Номер гнезда")
    percent_mass = models.IntegerField("Процент массы")
    # url = models.SlugField(max_length=150, blank=True)

    def __str__(self):
        return str(self.code_goods)

    class Meta:
        verbose_name = "Форма изделия"
        verbose_name_plural = "Формы изделий"


class GoodsCalendar(models.Model):
    """Календарь создания изделий"""
    code_goods = models.ForeignKey(Goods, verbose_name="Код изделия", on_delete=models.CASCADE)
    month = models.DateField("Месяц", help_text="Вписывать только месяц и год, день оставлть '01' ")
    lith = models.IntegerField("Отлито шт.")
    remote = models.IntegerField("Брак шт.")
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


# Заказчики
class Customer(models.Model):
    """Заказчики"""
    name = models.CharField("Имя заказчика", max_length=120)
    email = models.EmailField("Email", unique=True)
    phone_number = models.CharField("Номер телефона", max_length=15)
    representative = models.CharField("Представитель (ФИО)", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = 'Заказчики'


class CheckoutGoods(models.Model):
    """Заказчики и изделия"""
    customer_name = models.ForeignKey(Customer, verbose_name="Имя заказчика", on_delete=models.CASCADE)
    date = models.DateField("Дата заказа", default=default_datetime)
    code_goods = models.ManyToManyField(Goods, verbose_name="Код изделия")
    values = models.IntegerField("Количество")

    def __str__(self):
        return self.customer_name

    class Meta:
        verbose_name = "Дата заказа"
        verbose_name_plural = 'Даты заказов'
