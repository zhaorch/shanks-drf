import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction

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
    # user = UserNameSerializer(many=False,read_only=True)
    params = serializers.SerializerMethodField(read_only=True)

    def get_params(self, obj):
        all_params = App_Param.objects.filter(app_id=obj.id).select_related('app')
        # params_serializer = App_ParamNameSerializer(all_params, many=True, context={'request': self.context['request']})
        params_serializer = App_ParamNameSerializer(all_params, many=True)
        return params_serializer.data

    class Meta:
        model = App
        fields = "__all__"


class App_ParamCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=False,required=False)
    isSet = serializers.BooleanField(write_only=True)
    # isSet = serializers.BooleanField(read_only=True)
    class Meta:
        model = App_Param
        fields = "__all__"

class AppCreateSerializer(serializers.ModelSerializer):
    params = App_ParamCreateSerializer(many=True)
    class Meta:
        model = App
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data["user"]
        paramList = validated_data.pop("params")
        instance = App.objects.create(**validated_data)
        for param in paramList:
            if "isSet" in param.keys():
                isSet = param.pop("isSet")
            App_Param.objects.create(app=instance, **param)

        return instance

    # @transaction.atomic
    # def update(self, instance, validated_data):
    #     from rest_framework.utils import model_meta
    #     info = model_meta.get_field_info(instance)
    #
    #     for attr, value in validated_data.items():
    #         if attr in info.relations and info.relations[attr].to_many:
    #             field = getattr(instance, attr)
    #             field.set(value)
    #         else:
    #             setattr(instance, attr, value)
    #     instance.save()
    #     App_Param.objects.filter(app_id=instance.id).delete()
    #     paramList = validated_data.pop("params")
    #     for param in paramList:
    #         isSet = param.pop("isSet",false)
    #         if isSet:
    #             a=222
    #         App_Param.objects.create(app=instance, **param)
    #
    #     return instance

    # def update(self, instance, validated_data):
    #     # Updates an exisitng Company with several services
    #     instance.name = validated_data['name']
    #     instance.address = validated_data['address']
    #     instance.cost_per_patient = validated_data['cost_per_patient']
    #     instance.renting_fee = validated_data['renting_fee']
    #     services_data = validated_data['services']
    #
    #     for item in services_data:
    #         updatedService = ServiceType(
    #             serviceName=item['serviceName'],
    #             servicePrice=item['servicePrice'],
    #             id=item['id'],
    #             company=instance)
    #         updatedService.save()
    #
    #     return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'params' in validated_data:
            answer_ids_new = []
            answer_ids_pre = App_Param.objects.all().filter(app=instance).values_list('id', flat=True)
            for param in validated_data.pop('params'):
                isSet = param.pop("isSet",None)
                id = param.pop("id",None)
                param["app"]=instance
                ans, _created = App_Param.objects.update_or_create(id=id, defaults={**param})
                # if _created:
                #     ans.app = instance
                #     ans.save()
                answer_ids_new.append(ans.id)

            delete_ids = set(answer_ids_pre) - set(answer_ids_new)
            App_Param.objects.filter(id__in=delete_ids).delete()

        from rest_framework.utils import model_meta
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


