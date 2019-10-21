from django.urls import path
from . import views

urlpatterns = [
path("", views.home, name="home"),
path("create/", views.create, name="home"),
path("<int:id>", views.index, name="index"),
path("", views.button),
path("start/", views.insertion,name="start"),
path("pause/", views.pauseinsertion,name="pause"),
]

# path("", views.runmonitor)
# url(r'^$', views.cur_time, name='time'),
