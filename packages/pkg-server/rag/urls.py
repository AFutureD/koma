from django.urls import path

from . import views

urlpatterns = [
    path("memories/list", views.index, name="index"),
]