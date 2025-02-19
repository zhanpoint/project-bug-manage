import os
import sys
import django

# os.path.abspath(__file__) 获取当前文件的绝对路径，os.path.dirname(...) 获取当前文件所在目录的路径，再次调用 os.path.dirname(...) 获取上一级目录的路径。
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path指定 Python 解释器在导入模块时搜索的路径。将base_dir添加到 Python 的模块搜索路径中
sys.path.append(base_dir)

# 当os.environ.setdefault访问指定的环境变量时，就会从添加到 Python 的模块搜索路径中搜寻

# os.environ 用于访问和修改环境变量，
# setdefault检查环境变量 DJANGO_SETTINGS_MODULE 是否已经存在。如果该环境变量已经存在，则保持其现有值不变，否则将其设置为 "Bug_manage.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bug_manage.settings")
# 加载配置文件：读取并应用 DJANGO_SETTINGS_MODULE 环境变量中指定的设置模块Bug_manage.settings
django.setup()

# 由于Django的模型依赖于配置文件中的设置，所以在导入模型之前，需要先加载配置文件，并完成配置文件的初始化。
from web import models
# models.UserInfo.objects.create(username='admin', password='222333', phone='12345678901')
