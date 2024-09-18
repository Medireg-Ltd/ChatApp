from apps.accounts.custom_views import UserListView
from apps.accounts.views import LoginUserView, LogoutUserAPIView, RegisteruserView
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

project_router = SimpleRouter()
project_router.register(r"users", UserListView, basename="users")

urlpatterns = [
    path("register/", RegisteruserView.as_view()),
    path("login/", LoginUserView.as_view()),
    path("logout/", LogoutUserAPIView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(project_router.urls)),
]
