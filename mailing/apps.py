from time import sleep

from django.apps import AppConfig


class MailingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing"

    def ready(self):
        from mailing.management.commands.run_aps import Command
        # from django.core.management import call_command
        print('django-apscheduler запущен')
        sleep(2)
        # call_command('run_aps')
        Command().handle()
