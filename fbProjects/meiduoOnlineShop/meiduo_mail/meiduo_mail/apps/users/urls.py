from django.urls import path

from . import views

urlpatterns = [
    # 注册用户
    path("user/", views.UserView.as_view()),
]