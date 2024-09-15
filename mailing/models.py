from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """Клиенты сервиса"""
    email = models.EmailField(max_length=100, verbose_name='email')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия',
                                 **NULLABLE, help_text='Введите фамилию')
    first_name = models.CharField(max_length=150,
                                  **NULLABLE, verbose_name='Имя',
                                  help_text='Введите имя')
    patronymic = models.CharField(max_length=150,
                                  **NULLABLE, verbose_name='Отчество',
                                  help_text='Введите отчество')
    a_comment = models.TextField(verbose_name='Комментарий',
                                 help_text='Введите комментарий')
    date_of_birth = models.DateField(verbose_name='Дата рождения',
                                     **NULLABLE,
                                     help_text='Введите дату рождения')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

        # Сортировка
        ordering = [
            'first_name',
            'last_name',
            'patronymic',
            'date_of_birth',
        ]


class Message(models.Model):
    """Сообщения рассылки """
    letter_subject = models.CharField(
        max_length=255,
        verbose_name='Тема письма',
        help_text='Укажите тему письма')

    image_message = models.ImageField(
        upload_to='mailings/images',
        **NULLABLE, verbose_name='Изображение письма',
        help_text='Загрузите изображение письма'
    )
    letter_body = models.TextField(verbose_name='Тело письма',
                                   help_text='Введите текст письма')

    def __str__(self):
        return f'{self.letter_subject}'

    class Meta:
        verbose_name = 'Сообщение рассылки'
        verbose_name_plural = 'Сообщения рассылки'


class Mailing(models.Model):
    """Настройки для рассылки"""
    mailing_name = models.CharField(
        max_length=150,
        verbose_name='Название рассылки',
        help_text='Укажите название рассылки')

    datetime_first_mailing = models.DateTimeField(
        verbose_name='Дата и время отправки рассылки')

    next_datetime_first_mailing = models.DateTimeField(
        verbose_name='Дата и время следующей отправки рассылки')

    last_datetime_first_mailing = models.DateTimeField(
        verbose_name='Дата и время последней отправки рассылки')

    period_mailing_choices = (
        (1, 'Каждую минуту'),
        (60, 'Каждый час'),
        (1440, 'Ежедневно'),
        (10080, 'Еженедельно'),
        (43200, 'Ежемесячно(каждые 30 дней)'),
    )

    period_mailing = models.IntegerField(
        choices=period_mailing_choices,
        verbose_name='Период рассылки',
        help_text='Выберите период рассылки'
    )

    mailing_status_choices = (
        (0, 'Создана'),
        (1, 'Запущена'),
        (2, 'Отменена'),
        (3, 'Завершена')
    )

    mailing_status = models.IntegerField(
        choices=mailing_status_choices,
        verbose_name='Статус рассылки',
        help_text='Выберите статус рассылки'
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name='Сообщение рассылки',
        related_name='settings_message',
    )

    def __str__(self):
        return f'{self.mailing_name}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingAttempt(models.Model):
    """Попытки отправки письма"""
    datetime_attempt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время попытки отправки',
        editable=False
    )
    attempt_status = models.BooleanField(
        verbose_name='Статус попытки',
        editable=False
    )
    service_response = models.TextField(
        verbose_name='Ответ сервиса',
        null=True,
        editable=False
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name='Рассылка')

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Клиент'
    )

    def __str__(self):
        return (f'Попытка рассылки {self.pk} - {self.mailing} '
                f'от {self.datetime_attempt} для клиента {self.client} '
                f'{self.attempt_status}')

    class Meta:
        verbose_name = 'Попытка отправки письма'
        verbose_name_plural = 'Попытки отправки письма'
