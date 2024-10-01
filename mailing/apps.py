from time import sleep

from django.apps import AppConfig


class MailingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing"

    def ready(self):
        from mailing.management.commands.run_aps import Command
        sleep(2)
        Command().handle()
