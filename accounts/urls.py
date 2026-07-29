from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path(
        "register/",
        views.register,
        name="register",
    ),

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "logout/",
        LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    path(
        "authors/<str:username>/",
        views.author_profile,
        name="author_profile",
    ),
]