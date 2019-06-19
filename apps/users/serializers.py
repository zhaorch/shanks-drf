import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import timedelta
from rest_framework.validators import UniqueValidator

from shanksDRF.settings import REGEX_MOBILE

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    # 默认的日期格式就是 %Y-%m-%d
    # birthday = serializers.DateField(read_only=True, format='%Y-%m-%d')
    class Meta:
        model = User
        fields = ("id","username", "gender", "birthday", "email", "mobile", "type")
