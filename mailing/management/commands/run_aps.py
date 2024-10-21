from apscheduler.schedulers.background import (BackgroundScheduler,
                                               BlockingScheduler)
from django.core.management import BaseCommand
from mailing.services import send_mailing


# BlockingScheduler запуск из командной строки
class Command(BaseCommand):

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_mailing, 'interval', seconds=60)
        scheduler.start()
