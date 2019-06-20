__author__ = 'zrc'
__date__ = '2019/6/20 14:54'
import django_filters
from .models import App


class AppFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name='name', help_text="名称", lookup_expr='contains')

    class Meta:
        model = App
        fields = ['name']