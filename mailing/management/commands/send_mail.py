from smtplib import SMTPException

from django.core.mail import send_mail
from django.core.management import BaseCommand
from config import settings
from mailing.models import Mailing, MailingAttempt
from mailing.services import get_datetime


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Функция для запуска рассылки из командной строки"""

        current_datetime = get_datetime()

        # создание объекта и фильтрация рассылок из базы данных
        mailings = Mailing.objects.filter(
            datetime_first_mailing__lte=current_datetime).filter(
            mailing_status__in=[0, 1])

        for mailing in mailings:
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
