from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class App(models.Model):
    name = models.CharField(max_length=128, verbose_name="程序名称")
    name_exe = models.CharField(max_length=128, verbose_name="程序exe名称")
    path = models.CharField(max_length=128, verbose_name="程序路径")
    version = models.CharField(max_length=128, verbose_name="程序版本")
    user = models.ForeignKey(User, verbose_name="作者", null=True, blank=True, on_delete=models.SET_NULL)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '程序'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class App_Param(models.Model):
    name = models.CharField(max_length=128, verbose_name="参数名")
    value = models.CharField(max_length=128, verbose_name="参数值")
    desc = models.CharField(max_length=128, null=True, blank=True, verbose_name="参数说明")
    is_visiable = models.BooleanField(default=True, verbose_name="是否可见")
    app = models.ForeignKey(App, verbose_name="程序", null=True, blank=True, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '程序参数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name