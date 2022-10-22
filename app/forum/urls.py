from django.urls import path

from forum.views import Index, ThreadView, CategoryListView, CategoryView, GalleryView

app_name = "forum"

urlpatterns = [
    path("", Index.as_view(), name="home"),
    path("categories/", CategoryListView.as_view(), name="category"),
    path("gallery/", GalleryView.as_view(), name="gallery"),
    path("thread/<str:thread_name>", ThreadView.as_view(), name="thread"),
    path("category/<str:category_name>", CategoryView.as_view(), name="thread"),
]
