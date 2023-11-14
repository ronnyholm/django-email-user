from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class User(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
