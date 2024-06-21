from django.contrib.auth.models import AbstractUser
from django.db import models

from users.manager import UserManager

NULLABLE = {
    'blank': True,
    'null': True
}


class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='email address', unique=True)
    phone_number = models.CharField(verbose_name='phone number', max_length=12, **NULLABLE)
    verify_key = models.CharField(max_length=10, verbose_name='verification key', **NULLABLE)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
