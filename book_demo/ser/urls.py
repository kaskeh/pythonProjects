from django.urls import path, re_path
from . import views

urlpatterns = [
    path('students/', views.student2View.as_view),
    re_path(r"^student/(?P<pk>\d+)/$", views.Student1View.as_view()),
    # 对数据提交时，进行校验
    path('student3/', views.Student3View.as_view()),
    # 反序列化阶段
    re_path(r'^student4/(?P<pk>\d+)/$', views.Student4View.as_view()),
    # 一个序列化器同时实现序列化和反序列化
    path('student5/', views.Student5View.as_view()),
    # 使用模型类序列化器
    path('student6/', views.Student6View.as_view()),
]
