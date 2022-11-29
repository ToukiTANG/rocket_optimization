import os

from celery import Celery

# 整合Django与celery，识别并加载Django的配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rocket_optimization.settings')
# 实例化celery对象
app = Celery('op_celery')
# 加载celery配置（主要是消息队列和结果存储）
app.config_from_object('mycelery.config')
# 加载任务
app.autodiscover_tasks(['mycelery.optimization', ])

# 启动命令：celery -A mycelery.main worker -l info -P eventlet
