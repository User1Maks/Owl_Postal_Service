import pytz
from django.conf import settings
from datetime import datetime, timezone
from smtplib import SMTPException
from datetime import timedelta
from django.core.mail import send_mail

from mailing.models import Mailing, MailingAttempt


def get_datetime():
    """Функция для получения текущей даты и времени"""

    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    return current_datetime


def send_mailing():
    """Функция для отправки письма и проверки статусов рассылки"""

    current_datetime = get_datetime()

    # Фильтруем рассылки по статусу "Создана"
    mailings = Mailing.objects.filter(mailing_status=0)

    for mailing in mailings:
        if mailing.datetime_first_mailing <= current_datetime:
            mailing.mailing_status = 1  # Переключаем статут на "Запущено"
            mailing.save()

    mailings_1 = Mailing.objects.filter(
        datetime_first_mailing__lte=current_datetime).filter(
        mailing_status__in=[1])

    for mailing in mailings_1:

        # Увеличиваем время следующей рассылки на ее периодичность
        # mailing.next_datetime_mailing = mailing.datetime_first_mailing
        mailing.next_datetime_mailing += timedelta(
            minutes=mailing.period_mailing)

        # Если дата следующей рассылки превышает дату последней
        # рассылки, меняем статус на "Завершена"
        if mailing.next_datetime_mailing >= mailing.last_datetime_mailing:
            mailing.mailing_status = 3
        mailing.save()

        # Если рассылка не была найдена, пропускаем дальнейшие действия
        if mailing is False:
            continue

        # Проходим по всем клиентам, которым нужно отправить рассылку
        for client in mailing.clients.all():
            try:
                # Отправка письма
                server_response = send_mail(
                    subject=mailing.message.letter_subject,
                    message=mailing.message.letter_body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False,
                )

                # Создаем объект попытки отправки рассылки
                MailingAttempt.objects.create(
                    mailing=mailing,  # Указываем рассылку
                    client=client,  # Указываем клиента
                    service_response=str(server_response),  # Ответ сервера
                    attempt_status=True  # Письмо отправлено успешно
                )

            except SMTPException as e:
                # Если произошла ошибка при отправке письма
                MailingAttempt.objects.create(
                    mailing=mailing,  # Указываем рассылку
                    client=client,  # Указываем клиента
                    service_response=str(e),  # Ответ сервера с ошибкой
                    attempt_status=False  # Письмо не отправлено
                )
