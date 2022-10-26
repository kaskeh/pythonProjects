from django.contrib.auth.backends import ModelBackend
import re
from .models import User

def get_user_by_account(account):
    """
     通过传入的账号动态获取 user 模型对象
    :param account: 有可能是手机号， 有可能是用户名
    :return: user 或 None
    """
    try:
        if re.match(r"1[3-9]\d{9}$", account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None  # 如果没有查到返回None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """
    修改Django 的认证类，为实现多账号登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):

        # 获取到user
        user = get_user_by_account(username)
        if user and user.check_password(password):
            # 返回 user
            return user
