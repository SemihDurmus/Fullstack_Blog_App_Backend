from django.urls import path
from .views import RegisterView, ProfileView, UserGetUpdateDelete

urlpatterns = [
    path('register/', RegisterView),
    path('profile/', ProfileView),
    path('edit/', UserGetUpdateDelete),
]
