from django.shortcuts import render
from random import randint
from django_redis import get_redis_connection
from rest_framework.views import APIView
from rest_framework.response import Response
import logging

# from meiduo_mail.libs.yuntongxun.sms import CCP

logger = logging.getLogger("django")


# Create your views here.
class SMSCodeView(APIView):
    """ 短信验证码 """

    def get(self, request, mobile):
        # 1. 生成验证码, 当不够6位时，自动补零
        sms_code = "%06d" % randint(0, 999999)
        # 将验证码 输出在日志里，能够在没有 真实手机短信发送渠道时的测试手段
        logger.info(sms_code)
        # 2. 创建redis连接对象
        redis_conn = get_redis_connection("verify_codes")
        # 3. 把验证码存储到redis 数据库  （键名， 存活时间，值）
        redis_conn.setex("sms_%s" % mobile, 300, sms_code)
        # # 4. 利用容联运通讯发送短信验证码
        # # CCP().send_template_sms(self, 手机号, [验证码, 5], 1)
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # 5. 响应
        return Response({"message": "ok"})
