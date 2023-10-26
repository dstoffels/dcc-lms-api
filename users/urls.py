from django.urls import path
from .views import LoginView, RefreshView, RegistrationView

urlpatterns = [
    path("register", RegistrationView.as_view()),
    path("login", LoginView.as_view()),
    path("refresh", RefreshView.as_view()),
]
