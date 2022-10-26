from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    """
    自定义用户模型类
    继承的是django.contrib.auth.models.AbstractUser,这样可以使用Django自带的认证
    在settings中配置 AUTH_USER_MODEL = "users.User"
    """
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    email_active = models.BooleanField(default=False, verbose_name="邮箱激活状态")

    class Meta:  # 配置数据库表名，及设置模型在admin站点显示的中文名
        db_table = 'tb_user'
        verbose_name = "用户"
        verbose_name_plural = verbose_name
