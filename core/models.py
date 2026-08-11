from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        MANAGER = 'MANAGER', _('Manager')
        STAFF = 'STAFF', _('Staff')

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STAFF)