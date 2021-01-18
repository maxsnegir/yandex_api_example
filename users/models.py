from django.contrib.auth.models import AbstractUser
from django.db import models


class AdvUser(AbstractUser):
    class UserRole(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    role = models.TextField(choices=UserRole.choices,
                            default=UserRole.USER)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, )
    confirmation_code = models.UUIDField(blank=True, null=True)

    class Meta(AbstractUser.Meta):
        ordering = ['username']
