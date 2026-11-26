from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Project user model. Defined before the first migration: swapping it later is painful."""
