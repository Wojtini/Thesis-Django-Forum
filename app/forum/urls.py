from django.contrib import admin
from django.urls import path

from forum.views import Index

app_name = "forum"

urlpatterns = [
    path("", Index.as_view(), name="home")
]
