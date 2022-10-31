from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    # # 查询所有省
    # path("areas/", views.AreaListView.as_view()),
    # re_path("^areas/(?P<pk>\d+)/$", views.AreaDetailView.as_view()),
]

router = DefaultRouter()
# base_name参数在3.0后就被替换成basename
router.register(r"areas", views.AreaViewSet, basename="area")
urlpatterns += router.urls