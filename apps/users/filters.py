__author__ = 'zrc'
__date__ = '2019/6/4 9:19'

import django_filters
from django.db.models import Q

from .models import UserProfile


class UserFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    GENDER_CHOICES = (
        (0, '女'),
        (1, '男')
    )
    username = django_filters.CharFilter(field_name='username', help_text="名称", lookup_expr='contains')
    gender = django_filters.ChoiceFilter(field_name='gender', help_text="性别",choices=GENDER_CHOICES)

    class Meta:
        model = UserProfile
        fields = ['username', 'gender']