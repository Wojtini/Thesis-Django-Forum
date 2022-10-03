from django.urls import path, re_path

from forum import consumers
from forum.views import Index, ThreadView

app_name = "forum"

urlpatterns = [
    path("", Index.as_view(), name="home"),
    path("thread/<int:thread_id>", ThreadView.as_view(), name="thread"),
]

websocket_urlpatterns = [
    re_path(r"ws/thread/(?P<thread_id>\d+)/$", consumers.ThreadConsumer.as_asgi()),
]
