from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.CharField(
        max_length=250, default='https://www.kindpng.com/picc/m/105-1055656_account-user-profile-avatar-avatar-user-profile-icon.png')
    bio = models.TextField(blank=True)

    def __str__(self):
        return "{} {}".format(self.user, 'Profile')
