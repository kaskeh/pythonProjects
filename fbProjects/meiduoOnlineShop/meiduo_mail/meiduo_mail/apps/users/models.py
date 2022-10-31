from django.db import models
from django.contrib.auth.models import AbstractUser
# from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer   发现该库在2.0.0版本之后就将TimedJSONWebSignatureSerializer类弃用了，引导用户使用直接支持JWS/JWT的库
from authlib.jose import jwt, JoseError
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    """
    自定义用户模型类
    继承的是django.contrib.auth.models.AbstractUser,这样可以使用Django自带的认证
    在settings中配置 AUTH_USER_MODEL = "users.User"
    """
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    email_active = models.BooleanField(default=False, verbose_name="邮箱激活状态")

    class Meta:  # 配置数据库表名，及设置模型在admin站点显示的中文名
        db_table = 'tb_user'
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def generate_email_vertify_url(self):
        """ 生成邮箱激活链接 """
        # 1. 创建加密序列化器
        # serializer = TJWSSerializer(settings.SECRET_KET, 3600 * 24)

        # # 2. 调用dumps 方法进行加密，bytes
        # data = {"user_id": self.id, "email": self.email}
        # token = serializer.dumps(data).decode()

        # 签名算法
        header = {"alg": "HS256"}
        # 用于签名的密钥
        key = settings.SECRET_KEY
        # 待签名的数据负载
        data = {"user_id": self.id, "email": self.email}
        token = jwt.encode(header=header, payload=data, key=key)

        # 3. 凭借激活url
        url = "http://www.meiduo.com:8080/success_verify_email.html?token=" + token.decode()
        return url

    @staticmethod
    def check_verify_email_token(token):
        """ 对 token解密并查询对应的user """
        # 1. 创建加密序列化器
        # 2. 调用 loads解密
        try:
            secret = settings.SECRET_KEY
            data = jwt.decode(token, secret)
        except BadData:
            return None
        else:
            id = data.get("user_id")
            email = data.get("email")
            try:
                user = User.objects.get(id=id, eamil=email)
            except User.DoesNotExist:
                return None
            else:
                return user