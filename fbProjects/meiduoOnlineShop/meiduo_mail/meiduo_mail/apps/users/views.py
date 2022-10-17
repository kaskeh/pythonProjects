from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response

from .serializers import CreateUserSerializer
from .models import User

# Create your views here.


class UserView(CreateAPIView):
    """ 用户注册 """
    # 指定序列化器
    serializer_class = CreateUserSerializer


class UsernameCountView(APIView):
    """ 判断用户输入的名称是否已注册过"""
    def get(self, username):
        # 查询user表
        count = User.objects.filter(username=username).count()

        # 包装响应数据
        data = {
            "username": username,
            "count": count
        }

        # 响应
        return Response(data)
