from django.urls import path, re_path

from . import views

urlpatterns = [
    # 注册用户
    path("user/", views.UserView.as_view()),
    # 判断用户名是否已注册
    re_path(r"^usernames/(?P<username>\w{5, 20})/count/%", views.UsernameCountView.as_view()),
]