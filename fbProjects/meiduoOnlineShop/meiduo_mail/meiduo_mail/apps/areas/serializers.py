from rest_framework import serializers

from .models import Area


"""
在查询所有省时用的是 AreaSerializer

在查询单一省时, SubSerializer代表单个省 ---> AreaSerializer  省下面的所有市
在查询单一市时, SubSerializer代表单个市 ---> AreaSerializer  市下面的所有区

"""


# 因当前需要的均可从模型中映射的到，故使用ModelSerializer
class AreaSerializer(serializers.ModelSerializer):
    """ 省序列化器 """
    class Meta:
        model = Area
        fields = ["id", "name"]


class SubSerializer(serializers.ModelSerializer):
    # 130000
    # 河北省模型.subs.all()
    """ 详情视图使用的序列化器 """
    # 序列化器的嵌套
    subs = AreaSerializer(many=True)  # 查询多的一方，故many=True
    # subs = serializers.PrimaryKeyRelatedField()  # 只会序列化出 id
    # subs = serializers.StringRelatedField()  # 序列化的时模型中str方法返回值

    class Meta:
        model = Area
        fields = ["id", "name", "subs"]
