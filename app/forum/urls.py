from django.contrib import admin
from django.urls import path

from forum.views import Index

urlpatterns = [
    path("", Index.as_view())
]
