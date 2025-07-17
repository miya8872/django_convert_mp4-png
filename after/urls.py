from django.urls import path
from . import views

app_name = "after"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("result/<uuid:id>/", views.result, name="result"),
    path("progress/", views.progress, name="progress"),
    path("img/", views.img, name="img"),
    path("git_link", views.git_link, name="git_link"),
]
