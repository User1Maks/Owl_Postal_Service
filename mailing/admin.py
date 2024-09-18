from django.contrib import admin

from mailing.models import Client, Message


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
    list_filter = ('id', 'letter_subject', )
    search_fields = ('id', 'letter_subject',)