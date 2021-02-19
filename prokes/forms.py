from django import forms
from django.forms import DateField

from .models import Goods, GoodsCalendar


class GoodsNewForm(forms.ModelForm):
    """Форма создания нового изделия"""
    class Meta:
        model = Goods
        fields = ("code", "image", "weight_clean", "weight_clean", "norma_with_carpet",
                  "consumption_smesi", "one_person_norma", "defect_limit")
        # виджет нужен ТОЛЬКО для вывода стилей


class CalendarForm(forms.ModelForm):
    """Форма календаря"""
    class Meta:
        model = GoodsCalendar
        fields = ("code_goods", "month", "lith", "remote", "remote_percent",
                  "one_man_sr", "one_man_max", "two_man_sr", "two_man_max")
        widgets = {
            "month": forms.SelectDateWidget,
        }
        # виджет нужен ТОЛЬКО для вывода стилей


class GoodsForm(forms.ModelForm):
    """Форма изделий"""
    class Meta:
        model = Goods
        fields = ("code", "image", "weight_clean", "weight_clean", "norma_with_carpet",
                  "consumption_smesi", "one_person_norma", "defect_limit")
