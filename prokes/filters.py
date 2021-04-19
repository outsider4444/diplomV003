import django_filters

from .models import *


class OTKFilter(django_filters.FilterSet):
    class Meta:
        model = OTK
        fields = '__all__'
