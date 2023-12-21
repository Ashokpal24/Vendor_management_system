from django.urls import path
from django.http import HttpResponse
from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView
)

urlpatterns = [
    path("api/register",UserRegisterView.as_view()),
    path("api/login",UserLoginView.as_view()),
    path("api/logout",UserLogoutView.as_view()),


]