from django.urls import path

from . import views

urlpatterns = [
    # 发短信
    path(r"^smscode/(?P<mobile>1[3-9]\d{9)/$", views.SMSCodeView.as_view())
]