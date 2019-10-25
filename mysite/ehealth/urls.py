from django.urls import path
from . import views

urlpatterns = [
path("", views.home, name="home"),
path("create/", views.create, name="create"),
path("switch/", views.switch,name="switch"),
path("<int:id>", views.index, name="index"),
path("insertion/", views.insertion,name="insertion"),
path("history/", views.history,name="history"),
# path("", views.button),
]

# path("pause/", views.pauseinsertion,name="pause"),
# path("", views.runmonitor)
# url(r'^$', views.cur_time, name='time'),
