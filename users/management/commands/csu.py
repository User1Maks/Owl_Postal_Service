from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Класс для команд """

    def handle(self, *args, **options):
        """Команда для создания суперпользователя"""
        user = User.objects.create(
            email='admin@example.com',
            first_name='Admin',
            last_name='Adminov',
            is_staff=True,  # Только для персонала
            is_superuser=True,  # Только для администратора
            is_active=True  # Только для активного пользователя
        )

        user.set_password('pass')
        user.save()
