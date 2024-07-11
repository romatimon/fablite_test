from django.contrib.auth.hashers import make_password, check_password
from django.db import models

"""
User Model
---------

Модель, представляющая пользователя в системе.

Атрибуты:
    username (str): Уникальное имя пользователя.
    email (str): Уникальный адрес электронной почты пользователя.
    password_hash (str): Хеш пароля пользователя.

Методы:
    set_password(password: str) -> None:
        Устанавливает хеш пароля пользователя.
    check_password(password: str) -> bool:
        Проверяет, соответствует ли введенный пароль хэшированному паролю пользователя.
"""


class User(models.Model):
    """Модель пользователя."""
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=100)

    def set_password(self, password):
        """Метод устанавливает хеш пароля пользователя."""
        self.password = make_password(password)

    def check_password(self, password):
        """Метод проверяет соответствие введенного пароля пользователя."""
        return check_password(password, self.password)
