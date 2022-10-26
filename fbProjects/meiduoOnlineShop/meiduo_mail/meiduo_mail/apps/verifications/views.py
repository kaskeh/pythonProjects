
from django.shortcuts import render
from random import randint
from django_redis import get_redis_connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from celery_tasks.sms.tasks import send_sms_code

# from meiduo_mail.libs.yuntongxun.sms import CCP
from . import constants

logger = logging.getLogger("django")


# Create your views here.
class SMSCodeView(APIView):
    """ 短信验证码 """

    def get(self, request, mobile):

        # 1. 创建redis连接对象
        redis_conn = get_redis_connection("verify_codes")
        # 2. 先从resid获取发送标记 当前标记需要立即获得，故暂跟下方管道一同等待执行
        send_flag = redis_conn.get("send_flag_%s" % mobile)
        # # 但也尝试进行管道事务优化 数据存在redis是经过编码的，记得解码
        # pl.get("send_flag_%s" % mobile)
        # send_flag = pl.execute()[0]  # 元组

        # 3. 如果取到了标记，说明此手机号频繁发验证码
        if send_flag:
            return Response({"message": "手机频繁发送短信"}, status=status.HTTP_400_BAD_REQUEST)

        # 4. 生成验证码, 当不够6位时，自动补零
        sms_code = "%06d" % randint(0, 999999)
        # 将验证码 输出在日志里，能够在没有 真实手机短信发送渠道时的测试手段
        logger.info(sms_code)

        # 创建redis 管道：（把多次redis操作装入管道中，将来一次性去执行，减少redis连接操作，当前get，setex，setex操作都会进行重新连接数据库而造成较大的性能损失）
        pl = redis_conn.pipeline()

        # 5. 把验证码存储到redis 数据库  （键名， 存活时间，值）
        # redis_conn.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 6. 存储一个标记，表示此手机号已发送过短信，标记有效期期60s
        # redis_conn.setex("send_flag_%s" % mobile, constants.SEND_CODE_REDIS_INTERVAL, 1)
        pl.setex("send_flag_%s" % mobile, constants.SEND_CODE_REDIS_INTERVAL, 1)

        # 执行管道
        pl.execute()

        # # 7. 利用容联运通讯发送短信验证码
        # # CCP().send_template_sms(self, 手机号, [验证码, 5], 1)
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)

        # 触发异步任务，将异步任务添加到celery 任务队列broker
        # send_sms_code(mobile, sms_code)  # 调用普通函数而已
        send_sms_code.delay(mobile, sms_code)  # 触发异步任务

        # 8. 响应
        return Response({"message": "ok"}, status=status.HTTP_200_OK)
