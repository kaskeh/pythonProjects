from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import (CreateUserSerializer,
                          MyTokenObtainPairSerializer,
                          UserDetailSerializer,
                          EmailSerializer)
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


# GET /user/
class UserDetailView(RetrieveAPIView):
    """ 用户详情信息展示 """
    serializer_class = UserDetailSerializer
    # queryset = User.objects.all()
    permission_classes = [IsAuthenticated]  # 指定权限，只有通过认证的用户才能访问当前视图

    def get_object(self):
        """ 重写此方法返回，要展示的用户模型对象 """

        # 按照mixins.py 中响应返回流程中，从这个方法里得到 字典/模型对象 进行序列化
        # return self.request.user 视频中的这个 当时应还有其他后续操作，把请求中用户信息在用户表中进行查询得到相应的用户模型对象
        # 原该视图的设计逻辑中 是要求带有一个查询的pk信息，然后在数据集中查询单一数据然后序列化返回结果

        user = User.objects.get(id=self.request.user.id)
        return user  # self.request.user 代表本次请求的用户

# 提前进行as_view, 即可不用在url那边处理
MyTokenObtainPair = MyTokenObtainPairView.as_view()

# PUT
class EmailView(UpdateAPIView):
    """ 更新用户邮箱 """
    permission_classes = [IsAuthenticated]  # 指定权限，只有通过认证的用户才能访问当前视图
    serializer_class = EmailSerializer

    def get_object(self):
        """
        https://qa.1r1g.com/sf/ask/3659116121/
        视图本身没有任何问题。问题是如果一个用户没有登录，那么request.user就会指向一个AnonymousUser对象。您可以将其视为虚拟用户。然而，这个用户没有数据库表示，因为我们对用户一无所知。它更多地用于提供统一的接口。

        现在因为request.user是AnonymousUser，您的目标是更改该用户的密码，但您无法将其存储到数据库中，因此出现错误。

        因此，用户首先需要登录，然后request.user才是真正的用户，更新密码应该有效。
        :return:
        """
        # 下面这种写法会导致 raise NotImplementedError("Token users have no DB representation")
        # return self.request.user

        user = User.objects.get(id=self.request.user.id)
        return user  # self.request.user 代表本次请求的用户

class EmailVerifyView(APIView):
    """ 激活用户邮箱 """

    def get(self, request):
        # 获取前端查询字符串中传入的token
        tokon = request.query_params.get("token")
        # 把token解密，并查询对应的user
        user = User.check_verify_email_token(token)
        # 修改当前user 的email_active 为 True
        if user is None:
            return Response({"message": "激活失败"}, status=status.HTTP_400_BAD_REQUEST)
        user.eamil_active = True
        user.save()
