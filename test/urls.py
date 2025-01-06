from django.conf.urls import url
from .views import user

urlpatterns = [
    url(r'^register/', user.register, name='register'),
]
