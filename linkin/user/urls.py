from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.contrib.auth.decorators import login_required
from .views import home, profile, match, friends


urlpatterns = [
    path("", login_required(home.as_view()), name="home"),
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        auth_view.LoginView.as_view(template_name="user/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_view.LogoutView.as_view(template_name="user/logout.html"),
        name="logout",
    ),
    path("profile", login_required(profile.as_view()), name="profile"),
    path("match", login_required(match.as_view()), name="match"),
    path("friends", login_required(friends.as_view()), name="friends"),
]
