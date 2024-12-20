from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(verbose_name='email', unique=True)
    username = models.CharField(max_length=150, unique=True, verbose_name='username')
    first_name = models.CharField(max_length=30, verbose_name='first name')
    last_name = models.CharField(max_length=30, verbose_name='last name')

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email



