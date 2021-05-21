from django import forms
from django.forms import DateInput

from .models import GoodsCalendar, GoodsDefaultForm, Workers, CheckoutGoods, Goods, Customer, Materials, \
    Suppliers, GoodsStorage, Nariad, OTK, MaterialStorage


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
        widgets ={
            'birthday' : forms.TextInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(attrs={'type': 'email'}),
        }


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
    """Форма добавления изделия на склад"""

    class Meta:
        model = GoodsStorage
        fields = '__all__'
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer_checkout'].queryset = CheckoutGoods.objects.none()

        if 'goods_code' in self.data:
            try:
                goods_code = int(self.data.get('goods_code'))
                self.fields['customer_checkout'].queryset = CheckoutGoods.objects.filter(code_goods_id=goods_code).order_by('code_goods_id')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['customer_checkout'].queryset = self.instance.goods_code.checkoutgoods_set.order_by('code_goods_id')

        if 'customer_code' in self.data:
            try:
                customer_code = int(self.data.get('customer_code'))
                self.fields['customer_checkout'].queryset = CheckoutGoods.objects.filter(customer_name_id=customer_code).order_by('customer_name_id')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['customer_checkout'].queryset = self.instance.goods_code.checkoutgoods_set.order_by('customer_name_id')


# Склад материалов
class MaterialsStorageNewForm(forms.ModelForm):
    """Форма добавления материала на склад"""

    class Meta:
        model = MaterialStorage
        fields = '__all__'
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }


# Наряды
class NariadNewForm(forms.ModelForm):
    """Форма добавления нового наряда"""

    class Meta:
        model = Nariad
        fields = '__all__'
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }


# ОТК
class OTKNewForm(forms.ModelForm):
    """Форма добавления нового ОТК"""

    class Meta:
        model = OTK
        fields = '__all__'
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
            'goods_value': forms.TextInput(attrs={'type': 'number', 'id': 'id_goods_value2'})
        }
