from django.urls import path

from forum.views import Index, ThreadView, CategoryListView, CategoryView, GalleryView, AccountCreation, FileListView, \
    UserListView, UserEntriesView, EntryFormView

app_name = "forum"

urlpatterns = [
    path("", Index.as_view(), name="home"),
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("gallery/", GalleryView.as_view(), name="gallery"),
    path("filelist/", FileListView.as_view(), name="filelist"),
    path("users/", UserListView.as_view(), name="userlist"),
    path("user/<str:user_id>", UserEntriesView.as_view(), name="user_id"),
    path("thread/<str:thread_name>", ThreadView.as_view(), name="thread"),
    path("category/<str:category_name>", CategoryView.as_view(), name="category"),
    path("new_account", AccountCreation.as_view(), name="new_account"),
    path("forms/entryform/<str:thread_name>", EntryFormView.as_view(), name="entry_form"),
]
