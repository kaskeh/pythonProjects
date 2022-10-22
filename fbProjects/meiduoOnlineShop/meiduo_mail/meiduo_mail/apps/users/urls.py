from django.urls import path, re_path

from . import views

urlpatterns = [
    # 注册用户
    path("users/", views.UserView.as_view()),
    # 判断用户名是否已注册
    re_path(r"^usernames/(?P<username>\w{5,20})/count/$", views.UsernameCountView.as_view()),
    # 判断手机号是否已注册
    re_path(r"^mobiles/(?P<mobile>1[3-9]\d{9})/count/$", views.MobileCountView.as_view()),
]