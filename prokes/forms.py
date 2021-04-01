from django import forms
from django.forms import DateField

from .models import Goods, GoodsCalendar, GoodsDefaultForm, Workers, CheckoutGoods, Goods, Customer, Materials, \
    Suppliers, GoodsStorage


# Изделия
class GoodsForm(forms.ModelForm):
    """Форма изделий"""

    class Meta:
        model = Goods
        fields = '__all__'


class CalendarForm(forms.ModelForm):
    """Форма календаря"""

    class Meta:
        model = GoodsCalendar
        fields = '__all__'
        widgets = {
            "month": forms.SelectDateWidget,
        }
        # виджет нужен ТОЛЬКО для вывода стилей


class FormsGoodsForm(forms.ModelForm):
    """Форма вывода форм изделий"""

    class Meta:
        model = GoodsDefaultForm
        fields = '__all__'


# Сотрудники
class WorkersForm(forms.ModelForm):
    """Форма сотрудников"""

    class Meta:
        model = Workers
        fields = '__all__'


# Заказчики
class CustomerForm(forms.ModelForm):
    """Форма заказчика"""

    class Meta:
        model = Customer
        fields = '__all__'


class CheckoutForm(forms.ModelForm):
    """Форма добавления заказа"""

    class Meta:
        model = CheckoutGoods
        fields = '__all__'


# Материалы
class MaterialNewForm(forms.ModelForm):
    """Форма добавления материала"""

    class Meta:
        model = Materials
        fields = '__all__'


# Поставщики
class SupplierNewForm(forms.ModelForm):
    """Форма добавления поставщика"""

    class Meta:
        model = Suppliers
        fields = '__all__'


# Склад изделий
class GoodsStorageNewForm(forms.ModelForm):
    """Форма добавления материала на склад"""

    class Meta:
        model = GoodsStorage
        fields = '__all__'
