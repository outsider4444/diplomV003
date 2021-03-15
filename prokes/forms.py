from django import forms
from django.forms import DateField

from .models import Goods, GoodsCalendar, GoodsDefaultForm, Workers, CheckoutGoods, Goods


# Изделия

class GoodsForm(forms.ModelForm):
    """Форма изделий"""

    class Meta:
        model = Goods
        fields = ("code", "image", "weight_clean", "weight_clean",)


class CalendarForm(forms.ModelForm):
    """Форма календаря"""

    class Meta:
        model = GoodsCalendar
        fields = ("goods_code", "month", "lith", "remote", "remote_percent",
                  "one_man_sr", "one_man_max", "two_man_sr", "two_man_max")
        widgets = {
            "month": forms.SelectDateWidget,
        }
        # виджет нужен ТОЛЬКО для вывода стилей


class FormsGoodsForm(forms.ModelForm):
    """Форма вывода форм изделий"""

    class Meta:
        model = GoodsDefaultForm
        fields = ("goods_code", "duplicate", "cleaning_period", "number_nest", "percent_mass")


# Сотрудники
class WorkersForm(forms.ModelForm):
    """Форма сотрудников"""

    class Meta:
        model = Workers
        fields = ("code", "name", "email", "birthday", "category","salary")


# Заказчики
class CheckoutForm(forms.ModelForm):
    """Форма добавления заказа"""

    class Meta:
        model = CheckoutGoods
        fields = '__all__'
