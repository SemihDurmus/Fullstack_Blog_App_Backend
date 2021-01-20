from django.urls import path
from .views import RegisterView, ProfileView, UserGetUpdateDelete

urlpatterns = [
    path('register/', RegisterView),
    path('<int:id>/profile/', ProfileView),
    path('<int:id>/edit/', UserGetUpdateDelete),
]
