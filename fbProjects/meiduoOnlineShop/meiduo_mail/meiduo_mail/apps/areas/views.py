from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin


from .models import Area
from .serializers import AreaSerializer, SubSerializer

# Create your views here.


# class AreaListView(APIView):
#     """ 查询所有省 """
#
#     def get(self, request):
#         # 1. 获取指定的查询集
#         qs = Area.objects.filter(parent=None)
#         # 2. 创建序列化器进行序列化
#         serializer = AreaSerializer(qs, many=True)
#         # 3. 响应
#         return Response(serializer.data)
#
# class AreaDetailView(APIView):
#     """ 查询单一省或市 """
#
#     def get(self, request, pk):
#         # 1. 根据pk 查询出指定的省或市
#         try:
#             area = Area.objects.get(id=pk)
#         except Area.DoesNotExist:
#             return Response({"message": "无效pk"}, status=status.HTTP_400_BAD_REQUEST)
#         # 2. 创建序列化器进行序列化
#         serializer = SubSerializer(area)
#         # 3. 响应
#         return Response(serializer.data)

class AreaListView(GenericAPIView):
    """ 查询所有省 """

    # 指定序列化器
    serializer_class = AreaSerializer
    # 指定查询集
    queryset = Area.objects.filter(parent=None)

    def get(self, request):

        # 1. 获取指定的查询集
        # qs = Area.objects.filter(parent=None)
        qs = self.get_queryset()
        # 2. 创建序列化器进行序列化
        # serializer = AreaSerializer(qs, many=True)
        serializer = self.get_serializer(qs, many=True)
        # 3. 响应
        return Response(serializer.data)


class AreaDetailView(APIView):
    """ 查询单一省或市 """

    def get(self, request, pk):
        # 1. 根据pk 查询出指定的省或市
        try:
            area = Area.objects.get(id=pk)
        except Area.DoesNotExist:
            return Response({"message": "无效pk"}, status=status.HTTP_400_BAD_REQUEST)
        # 2. 创建序列化器进行序列化
        serializer = SubSerializer(area)
        # 3. 响应
        return Response(serializer.data)
