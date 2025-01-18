from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test/', include('test.urls', namespace='test')),
    url(r'^web/', include('web.urls', namespace='web')),
]
