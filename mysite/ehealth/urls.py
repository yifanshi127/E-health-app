from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.cur_time, name='time'),
]
