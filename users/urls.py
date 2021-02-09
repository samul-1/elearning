from django.urls import include, path, re_path, reverse
from . import views
from .forms import LoginFormWithPlaceholders
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            authentication_form=LoginFormWithPlaceholders,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("password_change/", views.change_password, name="change_password"),
    path("profile/", views.profile, name="profile"),
    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name="signup"),
    path("register/teacher/", views.teacher_register, name="teacher_signup"),
    re_path(
        r"^course_signup/(?P<course_id>\d+)/$",
        views.course_signup,
        name="course_signup",
    ),
]
