from django.db import models
from django.utils.translation import gettext_lazy as _
from base.models import AbstractBaseUser
from base_user.managers import CustomUserManager


class User(AbstractBaseUser):

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    email = models.EmailField(
        _("Email Address"), unique=True, null=True, blank=True)
    avatar = models.ImageField(
        upload_to="avatars/", default="avatars/default_profile_avatar.jpg")
    is_terms_agreed = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL)
    firebase_uid = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.email if self.email else str(self.id)
