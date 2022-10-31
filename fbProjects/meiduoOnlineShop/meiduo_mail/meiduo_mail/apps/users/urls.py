from django.urls import path, re_path

from . import views


urlpatterns = [
    # 注册用户
    path("users/", views.UserView.as_view()),
    # 用户JWT登录
    path("authorizations/", views.MyTokenObtainPairView.as_view()),
    # 获取用户详情
    path("user/", views.UserDetailView.as_view()),
    # 更新邮箱
    path("email/", views.EmailView.as_view()),
    # 更新邮箱状态
    path("emails/verification/", views.EmailVerifyView.as_view()),
    # 判断用户名是否已注册
    re_path(r"^usernames/(?P<username>\w{5,20})/count/$", views.UsernameCountView.as_view()),
    # 判断手机号是否已注册
    re_path(r"^mobiles/(?P<mobile>1[3-9]\d{9})/count/$", views.MobileCountView.as_view()),
]
