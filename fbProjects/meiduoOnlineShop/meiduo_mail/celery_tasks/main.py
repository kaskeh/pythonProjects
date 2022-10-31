from celery import Celery
import os

# 告诉celery，如果需要使用django 的配置文件，应该去那里加载
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mail.settings.dev')

# 1. 创建celery 实例对象
celery_app = Celery("meiduo")

# 2. 加载配置文件
celery_app.config_from_object("celery_tasks.config")

# 3. 自动注册异步任务
celery_app.autodiscover_tasks(["celery_tasks.sms", "celery_tasks.email"])
# celery_app.autodiscover_tasks(["celery_tasks.sms", "celery_tasks.esms"])
