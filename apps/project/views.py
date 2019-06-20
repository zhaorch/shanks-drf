from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets,status
from rest_framework import authentication,permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters,mixins
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.decorators import detail_route, list_route
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import App,App_Param
from .serializers import AppSerializer
from .filters import AppFilter

# Create your views here.
User = get_user_model()


class CommonUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        a = request.resolver_match.url_name
        return request.user.is_superuser == 1

    def has_object_permission(self, request, view, obj):
        # 任何请求都允许读取权限，
        # 所以我们总是允许 GET，HEAD 或 OPTIONS 请求。
        if request.method in permissions.SAFE_METHODS:
            return True
        #return obj.id == request.user.id
        return request.user.is_superuser == 1 or request.user.id == obj.user.id


class CommonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    page_query_param = "page"
    max_page_size = 100


class AppViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication,)
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,CommonPermission)
    permission_classes = (permissions.IsAdminUser,)

    queryset = App.objects.all().order_by('name', 'created_time').select_related('user')
    serializer_class = AppSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = AppFilter
    search_fields = ('name', 'name_exe')
    ordering_fields = ('name',)