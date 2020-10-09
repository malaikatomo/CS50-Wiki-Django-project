from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("CreatePage", views.newPage, name="create"),
    path("random", views.random, name="randomPage"),
    path("edit/<str:title>", views.editPage, name="edit")
]
