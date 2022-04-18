from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.db import models


class CustomUser(PermissionsMixin, AbstractBaseUser):
    """
    Abstract User model that defines comman attributes
    that can inhertited by other models. This model uses email
    inside of username for login and other authentication layers.
    """

    email = models.EmailField("email", unique=True)
    is_active = models.BooleanField("is_active", default=False)
    is_staff = models.BooleanField("is_staff", default=False)
    is_administrator = models.BooleanField("is_administrator", default=False)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    class Meta:
        abstract = True


class User(CustomUser):
    """ """

    first_name = models.CharField(max_length=64, default="new user first name")
    last_name = models.CharField(max_length=64, default="new user last name")
