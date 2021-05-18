import django_filters
from django.forms import DateInput

from .models import *


class SearchSuppliersDeliveryFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name="date", lookup_expr='gte', widget=DateInput(attrs={'type': 'date'})
    )
    end_date = django_filters.DateFilter(
        field_name="date", lookup_expr='lte', widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = DeliveriesMaterials
        exclude = ['supplier_name', 'date', 'code_material', 'values']


# Отчеты
class ReportRemoteGoodsFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name="date", lookup_expr='gte', widget=DateInput(attrs={'type': 'date'})
    )
    end_date = django_filters.DateFilter(
        field_name="date", lookup_expr='lte', widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = OTK
        exclude = ['date', 'nariad_code', 'goods_value', 'remote_value']


class ReportUsedMaterialFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name="date", lookup_expr='gte', widget=DateInput(attrs={'type': 'date'})
    )
    end_date = django_filters.DateFilter(
        field_name="date", lookup_expr='lte', widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Nariad
        exclude = ['code', 'worker_code', 'goods_code', 'material_code', 'goods_value', 'date', 'used_materials']
