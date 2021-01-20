from django.urls import path
from .views import RegisterView, ProfileView

urlpatterns = [
    path('register/', RegisterView),
    path('<int:id>/profile/', ProfileView),
]
