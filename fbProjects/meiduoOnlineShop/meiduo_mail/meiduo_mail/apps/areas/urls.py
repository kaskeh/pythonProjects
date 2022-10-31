from django.conf.urls import url

from . import views

urlpatterns = [
    # 查询所有省
    path("areas/", views.AreaListView.as_view()),
]