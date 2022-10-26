import logging

from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
import re
from django_redis import get_redis_connection

from meiduo_mail.utils.token import Create_token


class CreateUserSerializer(serializers.ModelSerializer):
    """ 注册序列化器 """

    # 序列化器的所有字段：["id", "username", "password", "password2", "mobile", "sms_code", "allow"]
    # 需要校验的字段：["username", "password", "password2", "mobile", "sms_code", "allow"]
    # 模型中已存在的字段：["id", "username", "password", "mobile"]

    # 需要序列化(即向前端传输的数据内容)的字段： ["id", "username", "mobile", "token"]
    # 需要反序列化(前端传来的数据内容)的字段： ["username", "password", "password2", "mobile", "sms_code", "allow"]
    # 模型中没有的需要新定义，write_only为True 标识 password2只会反序列化
    password2 = serializers.CharField(label="确认密码", write_only=True)
    sms_code = serializers.CharField(label="验证码", write_only=True)
    allow = serializers.CharField(label="同意协议", write_only=True)  # 约定前端会传来 "true" "false"
    token = serializers.CharField(label="token", read_only=True)

    class Meta:
        model = User  # 从User 模型中映射序列化器字段
        # fields = "__all__"  直接使用数据库所有字段
        fields = ["id", "username", "password", "password2", "mobile", "sms_code", "allow", "token"]
        extra_kwargs = {  # 修改字段限制选项
            "username": {
                "min_length": 5,
                "max_length": 20,
                "error_messages": {
                    "min_length": "仅允许5-20个字符的用户名",
                    "max_length": "仅允许5-20个字符的用户名",
                }
            },
            "password": {
                'write_only': True,
                "min_length": 8,
                "max_length": 20,
                "error_messages": {
                    "min_length": "仅允许8-20个字符的密码",
                    "max_length": "仅允许8-20个字符的密码",
                }
            }
        }

    def validate_mobile(self, value):
        """ 单独校验手机号 """
        if not re.match(r"1[3-9]\d{9}$", value):
            raise serializers.ValidationError("手机号格式错误")
        return value

    def validate_allow(self, value):
        """ 是否同意协议校验 """
        if value != "true":
            raise serializers.ValidationError("请同意用户协议")
        return value

    def validate(self, attrs):
        """ 校验密码两个是否相同 """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("两个密码不一致")

        # 校验验证码
        redis_conn = get_redis_connection("verify_codes")
        mobile = attrs["mobile"]
        real_sms_code = redis_conn.get("sms_%s" % mobile)
        # 向redis存储数据时都是已字符串进行存储，但取出数据是bytes类型 [bytes]

        # 先判断能不能从数据库获得验证码，后再判断是不是一致
        if real_sms_code is None or attrs["sms_code"] != real_sms_code.decode():
            raise serializers.ValidationError("验证码错误")

        return attrs

    def create(self, validated_data):
        # 把反序列化数据中不需要存储的 password2，sms_code， allow 从字段中移除
        del validated_data["password2"]
        del validated_data["sms_code"]
        del validated_data["allow"]

        # 先把密码取出来
        password = validated_data.pop("password")

        # 创建用户模型对象，给模型中的username和mobile 属性赋值
        user = User(**validated_data)
        user.set_password(password)  # 把密码加密后再赋值给user的password 属性
        user.save()  # 存储到数据库

        token = Create_token.get_token(user)

        user.token = token

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token

    def validate(self, attrs):
        """
        登录返回token 和referen
        :param attrs:
        :return:
        """

        data = super().validate(attrs)
        data["token"] = str(data["access"])
        data["user_id"] = self.user.id
        data["username"] = self.user.username

        return data


class UserDetailSerializer(serializers.ModelSerializer):
    """ 用户详情序列化器 """
    class Meta:
        model = User
        fields = ["id", "username", "mobile", "email", "email_active"]
