from django import forms
from django.forms import DateField

from .models import Goods, GoodsCalendar


class GoodsForm(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        model = Goods
        fields = ("code", "image", "url", "measurement")
        # виджет нужен ТОЛЬКО для вывода стилей


class CalendarForm(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        model = GoodsCalendar
        fields = ("code_goods", "month", "lith", "remote", "remote_percent",
                  "one_man_sr", "one_man_max", "two_man_sr", "two_man_max")
        widgets = {
            "month": forms.SelectDateWidget,
        }
        # виджет нужен ТОЛЬКО для вывода стилей
