from django.db import models
from datetime import datetime


# Create your models here.


def default_datetime():
    return datetime.now()


class Workers(models.Model):
    """Сотрудники"""
    code = models.IntegerField('Код сотрудника', unique=True)
    name = models.CharField('ФИО', max_length=100)
    email = models.EmailField('Email', blank=True)
    phone_number = models.CharField('Номер телефона', max_length=11, default='8')
    birthday = models.DateField('Дата рождения')
    category = models.CharField('Категория', max_length=50)
    salary = models.PositiveIntegerField('Оклад', help_text='Вводить в рублях')

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Materials(models.Model):
    """Материалы"""
    code = models.CharField('Код материала', max_length=120)
    weight = models.IntegerField('Вес смеси')
    batch_number = models.IntegerField('Номер партии')
    pallet_number = models.IntegerField('Номер поддона')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


class Goods(models.Model):
    """Изделия"""
    code = models.CharField('Код изделия', max_length=120)
    name = models.CharField('Название изделия', max_length=30)
    image = models.ImageField("Фотография изделия", upload_to="goods/", blank=True)
    weight_clean = models.FloatField('Вес чистой детали', default=0)
    norma_na_vigruzku = models.FloatField('Норма на выгрузку', default=0)
    used_materials = models.FloatField('Расход смеси', default=0)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'


class GoodsDefaultForm(models.Model):
    """Формы изделий"""
    goods_code = models.ForeignKey(Goods, verbose_name="Код изделия", on_delete=models.CASCADE,
                                   related_name='goods_forms')
    duplicate = models.CharField("Дубликат", max_length=150)
    cleaning_period = models.FloatField("Период чистки")
    number_nest = models.FloatField("Номер гнезда формы")
    percent_mass = models.IntegerField("Процент массы")

    def __str__(self):
        return str(self.goods_code)

    class Meta:
        verbose_name = "Форма изделия"
        verbose_name_plural = "Формы изделий"


class GoodsCalendar(models.Model):
    """Календарь создания изделий"""
    goods_code = models.ForeignKey(Goods, verbose_name="Код изделия", on_delete=models.CASCADE)
    month = models.DateField("Месяц", help_text="Вписывать только месяц и год, день оставлть '01' ")
    lith = models.IntegerField("Отлито шт.")
    remote = models.IntegerField("Брак шт.")
    remote_percent = models.FloatField("Брак %")
    one_man_sr = models.CharField("Смена выработки на 1 человека в СРЕДНЕМ", max_length=150)
    one_man_max = models.CharField("Смена выработки на 1 человека МАКСИМАЛЬНО", max_length=150)
    two_man_sr = models.CharField("Смена выработки на 2 человек в СРЕДНЕМ", max_length=150)
    two_man_max = models.CharField("Смена выработки на 2 человека МАКСИМАЛЬНО", max_length=150)

    def __str__(self):
        return str(self.month)

    class Meta:
        verbose_name = "Календарь изделий"
        verbose_name_plural = "Календарь изделий"


class Customer(models.Model):
    """Заказчики"""
    name = models.CharField("Имя заказчика", max_length=120)
    email = models.EmailField("Email", unique=True)
    phone_number = models.CharField("Номер телефона", max_length=11, default='8')
    representative = models.CharField("Представитель (ФИО)", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = 'Заказчики'


class CheckoutGoods(models.Model):
    """Заказчики и изделия"""
    customer_name = models.ForeignKey(Customer, verbose_name="Имя заказчика", on_delete=models.CASCADE)
    date = models.DateField("Дата заказа", default='')
    code_goods = models.ForeignKey(Goods, verbose_name="Код изделия", on_delete=models.SET_NULL, null=True)
    values = models.IntegerField("Количество")

    def __str__(self):
        header = str(self.date) + ' | ' + str(self.code_goods.code) + ' | ' + str(self.values)
        return header

    class Meta:
        verbose_name = "Дата заказа"
        verbose_name_plural = 'Даты заказов'


class Suppliers(models.Model):
    """Поставщики"""
    name = models.CharField('Наименование поставщика', max_length=150)
    email = models.EmailField('Email')
    phone_number = models.CharField('Номер телефона', max_length=11, default='8')
    representative = models.CharField("Представитель (ФИО)", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = 'Поставщики'


class DeliveriesMaterials(models.Model):
    """Поставщики и материалы"""
    supplier_name = models.ForeignKey(Suppliers, verbose_name="Имя поставщика", on_delete=models.CASCADE)
    date = models.DateField("Дата заказа", default=default_datetime)
    code_material = models.ForeignKey(Materials, verbose_name="Код смеси", on_delete=models.SET_NULL, null=True)
    values = models.IntegerField("Количество")

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "Дата поставки"
        verbose_name_plural = 'Даты поставок'


class Nariad(models.Model):
    """Наряды"""
    code = models.IntegerField('Номер наряда', unique=True)
    worker_code = models.ForeignKey(Workers, verbose_name='Код сотрудника', on_delete=models.SET_NULL, null=True)
    goods_code = models.ForeignKey(Goods, verbose_name='Код изделия', on_delete=models.SET_NULL, null=True)
    material_code = models.ForeignKey(Materials, verbose_name='Код материала', on_delete=models.SET_NULL, null=True)
    goods_value = models.IntegerField('Количество выпущенных изделий')
    date = models.DateField('Дата')
    used_materials = models.FloatField('Расход смеси', default=0)

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = "Наряд"
        verbose_name_plural = 'Наряды'


class OTK(models.Model):
    """ОТК"""
    nariad_code = models.OneToOneField(Nariad, verbose_name='Код наряда', on_delete=models.CASCADE)
    goods_value = models.IntegerField('Количество хороших изделий')
    remote_value = models.IntegerField('Количество бракованных изделий')
    date = models.DateField('Дата проверки')

    def __str__(self):
        return str(self.nariad_code)

    class Meta:
        verbose_name = "ОТК"
        verbose_name_plural = 'ОТК'


class MaterialStorage(models.Model):
    """Склад материалов"""
    material_code = models.ForeignKey(Materials, verbose_name='Код смеси', on_delete=models.CASCADE)
    supplier_code = models.ForeignKey(Suppliers, verbose_name='Код поставщика', on_delete=models.SET_NULL, null=True, blank=True)
    value = models.IntegerField('Количество', default=0)
    date = models.DateField('Дата проверки')

    def __str__(self):
        return str(self.material_code)

    class Meta:
        verbose_name = "Склад материалов"
        verbose_name_plural = 'Склады материалов'


class GoodsStorage(models.Model):
    """Склад изделий"""
    goods_code = models.ForeignKey(Goods, verbose_name='Код изделия', on_delete=models.CASCADE)
    value = models.IntegerField('Количество', default=0)
    customer_code = models.ForeignKey(Customer, verbose_name='Код заказчика', on_delete=models.SET_NULL, null=True)
    customer_checkout = models.OneToOneField(CheckoutGoods, verbose_name='Код заказа', on_delete=models.SET_NULL, null=True)
    date = models.DateField('Дата проверки')

    def __str__(self):
        return str(self.goods_code)

    class Meta:
        verbose_name = "Склад изделий"
        verbose_name_plural = 'Склады изделий'
