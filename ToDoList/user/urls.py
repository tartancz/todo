from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeView

from .views import (
    register_view,
    LoginModifiedView,
    ProfileView,
    update_profile_view,
    delete_profile,
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", LoginModifiedView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("profile/update/", update_profile_view, name="profile-update"),
    path(
        "profile/update-password/",
        PasswordChangeView.as_view(template_name="user/logged/change_password.html"),
        name="change-password",
    ),
    path("profile/delete-profile/", delete_profile, name="profile-delete"),
]
