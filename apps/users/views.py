from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters,mixins
from rest_framework import permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.hashers import make_password

from .serializers import UserSerializer
from .filters import UserFilter

# Create your views here.
User = get_user_model()


class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    page_query_param = "page"
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
    """
    用户
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = UserFilter
    search_fields = ('username', 'email')
    ordering_fields = ('id',)

    # /users/{pk}/userInfo/
    @detail_route(methods=['get'])
    def userInfo(self, request, pk=None):
        user =request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def reset_pwd(self, request, pk=None):
        # User.objects.filter(id=pk).update(password=make_password('123456'))
        # user = User.objects.filter(id=pk)
        # user.update(password = make_password('123456'))
        user = self.get_object()
        user.password = make_password('123456')
        user.save()
        serializer = UserSerializer(user, many=False)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    @detail_route(methods=['post'])
    def change_pwd(self, request, pk=None):
        password_old = self.request.query_params.get("password_old")
        password_new = self.request.query_params.get("password_new")
        user = self.get_object()
        if user.password == make_password(password_old):
            user.password = make_password(password_new)
            user.save()
            serializer = UserSerializer(user, many=False)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        else:
            return Response("原始密码错误",status=status.HTTP_400_BAD_REQUEST)

