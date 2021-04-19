import django_filters
from django.forms import DateInput
from django_filters import DateFilter

from .models import *


class OTKFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name="date", lookup_expr='gte', widget=DateInput(attrs={'type': 'date'})
    )
    end_date = django_filters.DateFilter(
        field_name="date", lookup_expr='lte', widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = OTK
        fields = '__all__'
        exclude = ['date', 'nariad_code', 'goods_value', 'remote_value']
