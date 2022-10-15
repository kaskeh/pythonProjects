from rest_framework.views import exception_handler as drf_exception_handler
import logging
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status

# 获取在配置文件中定义的logger，用来记录日志
logger = logging.getLogger("django")

def exception_handler(exc, context):
    """
    自定义异常处理，在原有drf异常捕获之外再进行的异常捕获
    :param exc: 异常实例对象
    :param context: 字典，抛出异常的上下文（包含request 和view 对象）
    :return: Response 响应对象
    """

    # 调用drf框架原生的异常处理方法
    response = drf_exception_handler(exc, context)

    if response is None:
        view = context["view"]
        # 捕获mysql， redis数据库异常
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 数据库异常
            logger.error("[%s] %s" % (view, exc))
            response = Response({"message": "服务器内部异常"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response