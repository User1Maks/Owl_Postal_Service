from django.contrib import admin

from mailing.models import Client, Message, Mailing, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'last_name', 'first_name', 'patronymic', 'date_of_birth')
    list_filter = ('id', 'email', 'last_name', 'date_of_birth',)
    search_fields = ('id', 'email', 'last_name', 'first_name', 'patronymic',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'letter_subject', 'image_message', 'letter_body',)
    list_filter = ('id', 'letter_subject',)
    search_fields = ('id', 'letter_subject',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing_name', 'datetime_first_mailing',
                    'next_datetime_mailing',
                    'last_datetime_mailing',
                    'period_mailing', 'mailing_status', 'message',)
    list_filter = ('id', 'mailing_name', 'datetime_first_mailing',
                   'next_datetime_mailing', 'last_datetime_mailing',
                   'period_mailing', 'mailing_status',)
    search_fields = ('id', 'mailing_name', 'mailing_status',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime_attempt', 'attempt_status', 'mailing', )
    list_filter = ('attempt_status', 'mailing',)
    search_fields = ('attempt_status', 'mailing', )
