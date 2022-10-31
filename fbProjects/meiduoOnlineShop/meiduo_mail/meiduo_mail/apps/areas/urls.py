from django.urls import path, re_path, include

from . import views

urlpatterns = [
    # 查询所有省
    path("areas/", views.AreaListView.as_view()),
    re_path("^areas/(?P<pk>\d+)/$", views.AreaDetailView.as_view()),
]