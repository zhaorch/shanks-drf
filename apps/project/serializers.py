import re
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import App,App_Param

User = get_user_model()


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username")


class App_ParamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = App_Param
        fields = ["id","name", "value", "desc", "is_visiable"]


class AppSerializer(serializers.ModelSerializer):
    user = UserNameSerializer()
    params = serializers.SerializerMethodField(read_only=True)

    def get_params(self, obj):
        all_params = App_Param.objects.filter(app_id=obj.id).select_related('app')
        # params_serializer = App_ParamNameSerializer(all_params, many=True, context={'request': self.context['request']})
        params_serializer = App_ParamNameSerializer(all_params, many=True)
        return params_serializer.data

    class Meta:
        model = App
        fields = "__all__"


class App_ParamSerializer(serializers.ModelSerializer):
    app = AppSerializer()

    class Meta:
        model = App_Param
        fields = "__all__"


