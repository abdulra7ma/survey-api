from django.urls import path
from .views import RegisterView, LogInView, AdministoratorRegisterView

urlpatterns = [
    path("register", RegisterView.as_view()),
    path("administorator-register", AdministoratorRegisterView.as_view()),
    path("login", LogInView.as_view()),
]
