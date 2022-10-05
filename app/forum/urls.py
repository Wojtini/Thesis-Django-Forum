from django.urls import path

from forum.views import Index, ThreadView, CategoryView, GalleryView

app_name = "forum"

urlpatterns = [
    path("", Index.as_view(), name="home"),
    path("categories/", CategoryView.as_view(), name="category"),
    path("gallery/", GalleryView.as_view(), name="gallery"),
    path('thread/<int:thread_id>', ThreadView.as_view(), name="thread"),
]
