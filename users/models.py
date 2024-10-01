from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(
        upload_to='users/avatars/',
        verbose_name='Аватар',
        **NULLABLE,
        help_text='Загрузите ваш аватар'
    )
    phone = PhoneNumberField(
        verbose_name='Телефон',
        **NULLABLE,
        region='RU',
        help_text='Введите номер телефона'
    )
    a_country = models.CharField(
        max_length=100,
        verbose_name='Страна',
        **NULLABLE,
        help_text='Введите страну проживания'
    )
    token = models.CharField(max_length=100, verbose_name='Token', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('can_edit_is_active_users',
             'Может блокировать пользователей сервиса'),

            ('can_edit_is_active_mailing', 'Может отключать рассылки')
        ]
