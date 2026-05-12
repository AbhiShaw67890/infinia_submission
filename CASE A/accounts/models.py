"""
accounts/models.py
Extends Django's AbstractUser with campus-specific profile fields.
Using AbstractUser (not AbstractBaseUser) keeps all Django auth behaviour
while letting us add avatar, college, phone, bio.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    """Campus user — inherits username, email, password from AbstractUser."""
    avatar = CloudinaryField('avatar', blank=True, null=True)
    college = models.CharField(max_length=120, blank=True)
    phone   = models.CharField(max_length=20, blank=True)
    bio     = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return self.username

    @property
    def avatar_url(self):
        """Returns avatar URL or a placeholder."""
        if self.avatar:
            return self.avatar.url
        return f"https://ui-avatars.com/api/?name={self.get_full_name() or self.username}&background=6366f1&color=fff&bold=true"
