from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import (CreateUserSerializer,
                          MyTokenObtainPairSerializer,
                          UserDetailSerializer)
from .models import User


# Create your views here.


class UserView(CreateAPIView):
    """ 用户注册 """
    # 指定序列化器
    serializer_class = CreateUserSerializer
    # queryset = User.objects.all()


class UsernameCountView(APIView):
    """ 判断用户输入的名称是否已注册过"""

    def get(self, request, username):
        # 查询user表
        count = User.objects.filter(username=username).count()

        # 包装响应数据
        data = {
            "username": username,
            "count": count
        }

        # 响应
        return Response(data)


class MobileCountView(APIView):
    """ 判断用户输入的手机号是否已注册过"""

    def get(self, request, mobile):
        # 查询user表
        count = User.objects.filter(mobile=mobile).count()

        # 包装响应数据
        data = {
            "mobile": mobile,
            "count": count
        }

        # 响应
        return Response(data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    # authentication_classes = (JWTAuthentication,)


class UserDetailView(RetrieveAPIView):
    """ 用户详情信息展示 """
    serializer_class = UserDetailSerializer
    # queryset = User.objects.all()
    permission_classes = [IsAuthenticated]  # 指定权限，只有通过认证的用户才能访问当前视图

    def get_object(self):
        """ 重写此方法返回，要展示的用户模型对象 """
        user = User.objects.get(id=self.request.user.id)
        return user  # self.request.user 代表本次请求的用户

        # return self.request.user

# 提前进行as_view, 即可不用在url那边处理
MyTokenObtainPair = MyTokenObtainPairView.as_view()
