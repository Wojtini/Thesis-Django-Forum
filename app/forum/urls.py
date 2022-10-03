from django.urls import path

from forum.views import Index, ThreadView

app_name = "forum"

urlpatterns = [
    path("", Index.as_view(), name="home"),
    path("thread/<int:thread_id>", ThreadView.as_view(), name="thread"),
]
