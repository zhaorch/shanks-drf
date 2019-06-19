from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    """
    用户
    """
    USER_TYPE = (
        (1, '加工人员'),
        (2, '质检人员'),
        (3, '开发人员'),
        (4, '管理员'),
    )
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.PositiveIntegerField(choices=((1, "男"), (0, "女")), default=1, verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    type = models.PositiveIntegerField(choices=USER_TYPE,default="1", verbose_name="人员类型")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
