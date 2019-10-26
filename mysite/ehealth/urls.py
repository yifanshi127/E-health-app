from django.urls import path
from . import views

urlpatterns = [
path("", views.home, name="home"),
path("create/", views.create, name="create"),
path("<int:id>", views.index, name="index"),
path("insertion/", views.insertion,name="insertion"),
path("history/", views.history,name="history"),
path("user/", views.user,name="user"),
path("update/", views.update,name="update"),
]

# path("", views.button),
# path("switch/", views.switch,name="switch"),
# path("pause/", views.pauseinsertion,name="pause"),
# path("", views.runmonitor)
# url(r'^$', views.cur_time, name='time'),
