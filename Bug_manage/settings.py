"""
Django settings for Bug_manage project.

Generated by 'django-admin startproject' using Django 1.11.28.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import redis
import django_redis

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qmt1o$jmdw!s+)8yf8e&eeyq0mm-e@9xvuix0_)(i8a(#%66_8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web.apps.WebConfig',
    'mptt',
    'bootstrap_pagination',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'web.middleware.web_middleware.AllMiddleWare'
]

ROOT_URLCONF = 'Bug_manage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, '/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Bug_manage.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# django项目配置数据库
from .local_settings import mysql_password

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    # Django需要通过MySQLdb模块与MySQL数据库进行交互，而这个模块在Windows环境下通常由mysqlclient库提供(记得安装)
    'db1': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'django',
        'USER': 'root',
        'PASSWORD': mysql_password,
    }
}

# django项目配置缓存
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 1000},
            'PASSWORD': '333444',
        }
    }
}
# 注意：如果是基于数据库的会话存储，只能使用数据库配置中的名为’default‘数据库
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_CACHE_ALIAS = 'default'  # 如果你使用的是基于缓存的会话存储，这将选择要使用的缓存。

SESSION_COOKIE_NAME = "sessionid"  # 会话cookie的名称，默认值为sessionid
SESSION_COOKIE_PATH = "/"  # 这个路径决定了浏览器在哪些 URL 路径下发送该会话 cookie。默认情况下值为 '/'，意味着会话cookie将被发送到站点下的所有路径。
SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名
SESSION_COOKIE_SECURE = False  # 是否支持Https传输cookie
SESSION_COOKIE_HTTPONLY = True  # 是否只支持Http传输cookie
SESSION_COOKIE_AGE = 1209600  # 设置session过期时间为2周（以秒为单位）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 关闭浏览器时不使session过期
SESSION_SAVE_EVERY_REQUEST = True  # Django会在每次请求时更新会话的过期时间

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#
LANGUAGE_CODE = 'zh-hans'

# 指定项目时区
TIME_ZONE = 'Asia/Shanghai'

# 不使用TIME_ZONE默认指定的时区（UTC）,而是自定义时区
USE_TZ = False

# 使用国际化功能
USE_I18N = True

# 使用本地化功能
USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# 定义了静态文件的URL前缀,所有静态文件都通过这个前缀访问
STATIC_URL = '/static/'

# 定义静态文件目录,默认是项目根目录下的static目录
# 这些目录通常用于存放项目级别的静态文件，而不是应用级别的静态文件。
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# 访问阿里云api接口的秘钥
ALIBABA_CLOUD_ACCESS_KEY_ID = ''
ALIBABA_CLOUD_ACCESS_KEY_SECRET = ''

# 发送短信的签名和模版ID
ALIYUN_SMS_SIGN1 = "sass平台"
ALIYUN_SMS_SIGN2 = "BugTracer平台"
ALIYUN_SMS_TEMPLATE = {
    "register": "SMS_474810651",
    "login": "SMS_474835623",
    "reset_password": "SMS_474835624"
}

# 用户登录时访问web应用中URL的白名单
prefix = '/web/'
WEB_WHITE_LIST = [

    'register/',
    'login/sms/',
    'login/name/',
    'imagecode/',
    'sms/',
    'index/',
]
WEB_WHITE_LIST = [prefix + i for i in WEB_WHITE_LIST]

"""
Django从3.2版本开始引入了DEFAULT_AUTO_FIELD设置，默认是AutoField，但推荐使用BigAutoField以避免主键溢出。
如果用户没有显式设置这个配置，或者没有在模型的Meta类中指定，就会触发这个警告
全局解决方案；在settings.py中添加 default_auto_field = 'django.db.models.BigAutoField'
特定模型解决方案：在每个模型的Meta类中指定 default_auto_field = 'django.db.models.BigAutoField'
修改DEFAULT_AUTO_FIELD后必须进行数据库迁移
"""
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 确保CSRF设置正确
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8004'  # Django开发服务器
]
# 允许跨域
CORS_ALLOW_CREDENTIALS = True  # 允许携带凭证
CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:8004'
]

try:
    from .local_settings import *
except ImportError:
    pass
